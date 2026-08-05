import json
import logging
import httpx
import uuid
from datetime import datetime
from typing import Optional

from app.core.config import settings
from app.schemas.ai_response import AIAnalysisResponse
from app.prompts.resume_prompt import ResumeAnalysisPrompt


logger = logging.getLogger(__name__)


class OpenRouterException(Exception):
    """Base exception for OpenRouter service."""

    pass


class OpenRouterAuthError(OpenRouterException):
    """Authentication error (401)."""

    pass


class OpenRouterForbiddenError(OpenRouterException):
    """Forbidden error (403)."""

    pass


class OpenRouterRateLimitError(OpenRouterException):
    """Rate limit error (429)."""

    pass


class OpenRouterServerError(OpenRouterException):
    """Server error (500)."""

    pass


class OpenRouterTimeoutError(OpenRouterException):
    """Request timeout error."""

    pass


class OpenRouterParseError(OpenRouterException):
    """Response parsing error."""

    pass


class OpenRouterService:
    """Service for interacting with OpenRouter API for resume analysis."""

    MAX_RETRIES: int = 1
    TIMEOUT: float = 60.0
    CONNECTION_TIMEOUT: float = 10.0

    def __init__(self) -> None:
        """Initialize OpenRouter service with connection pool."""
        self._client: Optional[httpx.AsyncClient] = None
        self._api_key = settings.openrouter_api_key
        self._model = settings.openrouter_model
        self._base_url = settings.openrouter_url

        if not self._api_key:
            raise ValueError("OPENROUTER_API_KEY environment variable not set")
        if not self._model:
            raise ValueError("OPENROUTER_MODEL environment variable not set")

    @property
    async def client(self) -> httpx.AsyncClient:
        """Get or create async HTTP client with connection pooling."""
        if self._client is None:
            limits = httpx.Limits(max_connections=10, max_keepalive_connections=5)
            self._client = httpx.AsyncClient(
                limits=limits,
                timeout=httpx.Timeout(
                    timeout=self.TIMEOUT, connect=self.CONNECTION_TIMEOUT
                ),
            )
        return self._client

    async def close(self) -> None:
        """Close HTTP client connection."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None

    def _get_headers(self) -> dict:
        """
        Build request headers for OpenRouter API.

        Returns:
            Dictionary of request headers
        """
        return {
            "Authorization": f"Bearer {self._api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost:3000",
            "X-Title": "RoleMatch AI",
        }

    def _build_request_payload(self, system_prompt: str, user_prompt: str) -> dict:
        """
        Build the request payload for OpenRouter API.

        Args:
            system_prompt: System prompt for the model
            user_prompt: User prompt with analysis request

        Returns:
            Dictionary containing the API request payload
        """
        return {
            "model": self._model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.3,
            "max_tokens": 4000,
        }

    async def _handle_error_response(self, status_code: int, response_text: str) -> None:
        """
        Handle error responses from OpenRouter API.

        Args:
            status_code: HTTP status code
            response_text: Response body text

        Raises:
            Appropriate exception based on status code
        """
        if status_code == 401:
            raise OpenRouterAuthError(
                f"Authentication failed: Invalid or expired API key"
            )
        elif status_code == 403:
            raise OpenRouterForbiddenError(
                f"Access forbidden: {response_text}"
            )
        elif status_code == 429:
            raise OpenRouterRateLimitError(
                f"Rate limit exceeded: Please retry after some time"
            )
        elif status_code == 500:
            raise OpenRouterServerError(
                f"Server error: OpenRouter API returned 500"
            )
        else:
            raise OpenRouterException(
                f"Unexpected error (status {status_code}): {response_text}"
            )

    async def call_model(
        self, job_title: str, resume_data: dict, request_id: Optional[str] = None
    ) -> dict:
        """
        Call OpenRouter API with resume analysis request.

        Args:
            job_title: Target job title
            resume_data: Structured resume data
            request_id: Optional request ID for logging

        Returns:
            Parsed response from OpenRouter API

        Raises:
            Various OpenRouterException subclasses on error
        """
        if not request_id:
            request_id = str(uuid.uuid4())

        start_time = datetime.now()
        system_prompt, user_prompt = ResumeAnalysisPrompt.get_prompts(
            job_title, resume_data
        )
        payload = self._build_request_payload(system_prompt, user_prompt)

        logger.info(
            f"[{request_id}] Starting OpenRouter API call | "
            f"Model: {self._model} | Job: {job_title}"
        )

        attempt = 0
        last_error = None

        while attempt <= self.MAX_RETRIES:
            try:
                attempt += 1
                client = await self.client
                response = await client.post(
                    self._base_url,
                    headers=self._get_headers(),
                    json=payload,
                )

                elapsed_time = (datetime.now() - start_time).total_seconds()

                if response.status_code >= 400:
                    await self._handle_error_response(
                        response.status_code, response.text
                    )

                logger.info(
                    f"[{request_id}] OpenRouter API call succeeded | "
                    f"Status: {response.status_code} | "
                    f"Latency: {elapsed_time:.2f}s | "
                    f"Attempt: {attempt}"
                )

                return response.json()

            except httpx.TimeoutException as e:
                last_error = e
                if attempt <= self.MAX_RETRIES:
                    logger.warning(
                        f"[{request_id}] Request timeout on attempt {attempt}, retrying..."
                    )
                else:
                    raise OpenRouterTimeoutError(
                        f"Request timed out after {attempt} attempts"
                    ) from e

            except (OpenRouterAuthError, OpenRouterForbiddenError) as e:
                logger.error(f"[{request_id}] Authentication/Authorization error: {e}")
                raise

            except OpenRouterRateLimitError as e:
                logger.warning(f"[{request_id}] Rate limit hit: {e}")
                if attempt <= self.MAX_RETRIES:
                    logger.info(f"[{request_id}] Retrying after rate limit...")
                else:
                    raise

            except OpenRouterException as e:
                logger.error(f"[{request_id}] OpenRouter service error: {e}")
                raise

        raise last_error or OpenRouterException("Unknown error occurred")

    def parse_response(self, api_response: dict, request_id: str = "") -> AIAnalysisResponse:
        """
        Parse and validate OpenRouter API response.

        Args:
            api_response: Raw response from OpenRouter API
            request_id: Request ID for logging

        Returns:
            Validated AIAnalysisResponse object

        Raises:
            OpenRouterParseError: If response cannot be parsed or validated
        """
        try:
            if not api_response or "choices" not in api_response:
                raise OpenRouterParseError("Invalid API response structure")

            choices = api_response.get("choices", [])
            if not choices:
                raise OpenRouterParseError("No choices in API response")

            message_content = choices[0].get("message", {}).get("content", "")
            if not message_content:
                raise OpenRouterParseError("No content in API response message")

            analysis_json = json.loads(message_content)

            response = AIAnalysisResponse(**analysis_json)

            logger.info(
                f"[{request_id}] Response parsing succeeded | "
                f"Match Score: {response.overall_match}%"
            )

            return response

        except json.JSONDecodeError as e:
            logger.error(f"[{request_id}] Failed to parse response JSON: {e}")
            raise OpenRouterParseError(f"Invalid JSON in API response: {e}") from e

        except ValueError as e:
            logger.error(f"[{request_id}] Response validation failed: {e}")
            raise OpenRouterParseError(f"Response validation error: {e}") from e

    async def analyze_resume(
        self, job_title: str, resume_data: dict
    ) -> AIAnalysisResponse:
        """
        Perform complete resume analysis using OpenRouter.

        Args:
            job_title: Target job title
            resume_data: Structured resume data from parser

        Returns:
            Validated AI analysis response

        Raises:
            Various OpenRouterException subclasses on error
        """
        request_id = str(uuid.uuid4())

        try:
            api_response = await self.call_model(job_title, resume_data, request_id)
            analysis_response = self.parse_response(api_response, request_id)
            return analysis_response

        except OpenRouterException as e:
            logger.error(f"[{request_id}] Analysis failed: {e}")
            raise

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
