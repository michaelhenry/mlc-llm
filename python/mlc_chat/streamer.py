"""Streamers in MLC LLM."""
from typing import List, Union

import tvm
import tvm._ffi
from tvm.runtime import Object, ShapeTuple

from . import _ffi_api
from .tokenizer import Tokenizer


@tvm._ffi.register_object("mlc.TextStreamer")  # pylint: disable=protected-access
class TextStreamer(Object):
    """The class that streams back validated utf-8 text strings
    that generated by tokenizer.
    """

    def __init__(self, tokenizer: Tokenizer) -> None:
        """Create the text streamer from tokenizer"""
        self.__init_handle_by_constructor__(
            _ffi_api.TextStreamer, tokenizer  # type: ignore  # pylint: disable=no-member
        )

    def put(self, delta_tokens: Union[List[int], ShapeTuple]) -> str:
        """Put new delta tokens into the streamer, and get the UTF-8-valid
        delta string. The text streamer may hold some of the input delta tokens
        which cannot decode into valid UTF-8 strings. The returned string
        is always guaranteed to be UTF-8 valid.

        Parameters
        ----------
        delta_tokens : Union[List[int], ShapeTuple]
            The new tokens to put into the streamer.

        Returns
        -------
        delta_text : str
            The decoded delta string after putting the input new tokens.
        """
        if isinstance(delta_tokens, list):
            delta_tokens = ShapeTuple(delta_tokens)
        return _ffi_api.TextStreamerPut(  # type: ignore  # pylint: disable=no-member
            self, delta_tokens
        )

    def finish(self) -> str:
        """Return the string decoded by remaining tokens."""
        return _ffi_api.TextStreamerFinish(self)  # type: ignore  # pylint: disable=no-member


@tvm._ffi.register_object("mlc.StopStringHandler")  # pylint: disable=protected-access
class StopStringHandler(Object):
    """The stop string handler in MLC LLM, which takes input delta text
    one at a time, and return the output delta text before stopping due to
    stop strings."""

    def __init__(self, stop_strs: List[str]) -> None:
        self.__init_handle_by_constructor__(
            _ffi_api.StopStringHandler, stop_strs  # type: ignore  # pylint: disable=no-member
        )

    def put(self, input_delta_text: str) -> str:
        """Add new input delta text to the handler, return output
        delta text before stopping. The stop string handler may hold
        some of the input delta text which may be part of a stop string.
        The returned string is always guaranteed not to be part of stop string.
        """
        return _ffi_api.StopStringHandlerPut(  # type: ignore  # pylint: disable=no-member
            self, input_delta_text
        )

    def finish(self) -> str:
        """Stop string handling has finished, return remaining string."""
        return _ffi_api.StopStringHandlerFinish(self)  # type: ignore  # pylint: disable=no-member

    @property
    def stop_triggered(self) -> bool:
        """Check if the generation has stopped due to stop string."""
        return _ffi_api.StopStringHandlerStopTriggered(self)  # type: ignore  # pylint: disable=no-member