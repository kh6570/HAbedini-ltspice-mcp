# In the name of God, the Most Gracious, the Most Merciful
"""Runtime configuration for ltspice-mcp."""

from __future__ import annotations

from pathlib import Path
from typing import ClassVar, Literal, Self

from mcp_app_core.settings import AppSettings
from platformdirs import user_cache_dir
from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict


class LTspiceFeatures(BaseModel):
    """Feature toggles that the server definition exposes."""

    schematic_inspection: bool = True
    waveform_parsing: bool = True
    simulation: bool = True


class LTspiceSettings(AppSettings):
    """The application settings. The environment and the CLI overrides load these settings."""

    session_mode: Literal["cold", "auto"] = "cold"
    recipe_path: Path | None = None
    telemetry_enabled: bool = False
    active_profiles: str = "default"
    window_sync: bool = False
    cache_app_name: ClassVar[str] = "ltspice-mcp"

    model_config = SettingsConfigDict(
        env_prefix="LTSPICE_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    def normalized(self) -> Self:
        """Return a copy with normalized paths and derived defaults."""

        cache_dir = self.cache_dir
        if cache_dir is None:
            cache_dir = Path(user_cache_dir("ltspice-mcp"))
        exe = self.exe.resolve(strict=False) if self.exe is not None else None
        log_folder = self.log_folder.resolve(strict=False) if self.log_folder is not None else None
        recipe_path = (
            self.recipe_path.resolve(strict=False) if self.recipe_path is not None else None
        )
        return self.model_copy(
            update={
                "exe": exe,
                "workspace_root": self.workspace_root.resolve(strict=False),
                "cache_dir": cache_dir.resolve(strict=False),
                "log_folder": log_folder,
                "recipe_path": recipe_path,
            }
        )

    def active_profile_names(self) -> tuple[str, ...]:
        """Return the profiles that a normal session or an extended session has to load."""

        names = tuple(part.strip() for part in self.active_profiles.split(",") if part.strip())
        if not names:
            raise ValueError("active_profiles must name at least one profile.")
        return names

    def resolve_timeout_s(self, explicit: float | None) -> float | None:
        """Return an explicit per-call timeout or the configured default.

        Non-positive values disable the timeout for that resolution path.
        """

        if explicit is not None:
            return None if explicit <= 0 else explicit
        configured = self.timeout_s
        if configured is not None and configured <= 0:
            return None
        return configured

    def with_cli_overrides(
        self,
        *,
        transport: Literal["stdio", "sse"] | None = None,
        exe: Path | None = None,
        workspace_root: Path | None = None,
        log_level: Literal["debug", "info", "warning", "error"] | None = None,
        telemetry_enabled: bool | None = None,
        log_folder: Path | None = None,
        recipe_path: Path | None = None,
        enable_sse: bool | None = None,
        session_mode: Literal["cold", "auto"] | None = None,
        active_profiles: str | None = None,
        window_sync: bool | None = None,
    ) -> Self:
        """Apply explicit CLI overrides on top of the settings that the environment loads."""

        updates: dict[str, object] = {}
        if transport is not None:
            updates["transport"] = transport
        if session_mode is not None:
            updates["session_mode"] = session_mode
        if active_profiles is not None:
            updates["active_profiles"] = active_profiles
        if window_sync is not None:
            updates["window_sync"] = window_sync
        if exe is not None:
            updates["exe"] = exe
        if workspace_root is not None:
            updates["workspace_root"] = workspace_root
        if log_level is not None:
            updates["log_level"] = log_level
        if telemetry_enabled is not None:
            updates["telemetry_enabled"] = telemetry_enabled
        if log_folder is not None:
            updates["log_folder"] = log_folder
        if recipe_path is not None:
            updates["recipe_path"] = recipe_path
        if enable_sse is not None:
            updates["enable_sse"] = enable_sse
        return self.model_copy(update=updates).normalized()


def build_settings(
    *,
    transport: Literal["stdio", "sse"] | None = None,
    exe: Path | None = None,
    workspace_root: Path | None = None,
    log_level: Literal["debug", "info", "warning", "error"] | None = None,
    telemetry_enabled: bool | None = None,
    log_folder: Path | None = None,
    recipe_path: Path | None = None,
    enable_sse: bool | None = None,
    session_mode: Literal["cold", "auto"] | None = None,
    active_profiles: str | None = None,
    window_sync: bool | None = None,
) -> LTspiceSettings:
    """Load settings from the environment and apply explicit CLI overrides."""

    return LTspiceSettings().with_cli_overrides(
        transport=transport,
        exe=exe,
        workspace_root=workspace_root,
        log_level=log_level,
        telemetry_enabled=telemetry_enabled,
        log_folder=log_folder,
        recipe_path=recipe_path,
        enable_sse=enable_sse,
        session_mode=session_mode,
        active_profiles=active_profiles,
        window_sync=window_sync,
    )
