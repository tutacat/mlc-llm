"""Environment variables used by the MLC LLM."""

import os
import sys
from pathlib import Path
from typing import List


def _check():
    if MLC_JIT_POLICY not in ["ON", "OFF", "REDO", "READONLY"]:
        raise ValueError(
            'Invalid MLC_JIT_POLICY. It has to be one of "ON", "OFF", "REDO", "READONLY"'
            f"but got {MLC_JIT_POLICY}."
        )


def _get_cache_dir() -> Path:
    if "MLC_LLM_HOME" in os.environ:
        result = Path(os.environ["MLC_LLM_HOME"])
    elif sys.platform == "win32":
        result = Path(os.environ["LOCALAPPDATA"])
        result = result / "mlc_llm"
    elif os.getenv("XDG_CACHE_HOME", None) is not None:
        result = Path(os.getenv("XDG_CACHE_HOME"))
        result = result / "mlc_llm"
    else:
        result = Path(os.path.expanduser("~/.cache"))
        result = result / "mlc_llm"
    result.mkdir(parents=True, exist_ok=True)
    if not result.is_dir():
        raise ValueError(
            f"The default cache directory is not a directory: {result}. "
            "Use environment variable MLC_LLM_HOME to specify a valid cache directory."
        )
    (result / "model_weights").mkdir(parents=True, exist_ok=True)
    (result / "model_lib").mkdir(parents=True, exist_ok=True)
    return result


def _get_dso_suffix() -> str:
    if "MLC_DSO_SUFFIX" in os.environ:
        return os.environ["MLC_DSO_SUFFIX"]
    if sys.platform == "win32":
        return "dll"
    if sys.platform == "darwin":
        return "dylib"
    return "so"


def _get_test_model_path() -> List[Path]:
    if "MLC_TEST_MODEL_PATH" in os.environ:
        return [Path(p) for p in os.environ["MLC_TEST_MODEL_PATH"].split(os.pathsep)]
    # by default, we reuse the cache dir via mlc_llm chat
    # note that we do not auto download for testcase
    # to avoid networking dependencies
    return [
        _get_cache_dir() / "model_weights" / "mlc-ai",
        Path(os.path.abspath(os.path.curdir)),
    ]


MLC_TEMP_DIR = os.getenv("MLC_TEMP_DIR", None)
MLC_MULTI_ARCH = os.environ.get("MLC_MULTI_ARCH", None)
MLC_LLM_HOME: Path = _get_cache_dir()
MLC_JIT_POLICY = os.environ.get("MLC_JIT_POLICY", "ON")
MLC_DSO_SUFFIX = _get_dso_suffix()
MLC_TEST_MODEL_PATH: List[Path] = _get_test_model_path()


_check()
