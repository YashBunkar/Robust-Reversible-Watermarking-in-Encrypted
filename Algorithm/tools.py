
import base64
import itertools
from functools import reduce
from typing import IO, Iterator, List, Tuple, Union

from PIL import Image

ENCODINGS = {"UTF-8": 8, "UTF-32LE": 32}


def a2bits(chars: str) -> str:
   
    return bin(reduce(lambda x, y: (x << 8) + y, (ord(c) for c in chars), 1))[3:]


def a2bits_list(chars: str, encoding: str = "UTF-8") -> List[str]:
    
    return [bin(ord(x))[2:].rjust(ENCODINGS[encoding], "0") for x in chars]


def bs(s: int) -> str:

    return str(s) if s <= 1 else bs(s >> 1) + str(s & 1)


def setlsb(component: int, bit: str) -> int:
    """Set Least Significant Bit of a colour component.
    """
    return component & ~1 | int(bit)


def n_at_a_time(
    items: List[int], n: int, fillvalue: str
) -> Iterator[Tuple[Union[int, str]]]:

    it = iter(items)
    return itertools.zip_longest(*[it] * n, fillvalue=fillvalue)


def binary2base64(binary_file: str) -> str:

    # Use mode = "rb" to read binary file
    with open(binary_file, "rb") as bin_file:
        encoded_string = base64.b64encode(bin_file.read())
    return encoded_string.decode()


def base642binary(b64_fname: str) -> bytes:

    b64_fname += "==="
    return base64.b64decode(b64_fname)


def open_image(fname_or_instance: Union[str, IO[bytes]]):

    if isinstance(fname_or_instance, Image.Image):
        return fname_or_instance

    return Image.open(fname_or_instance)
