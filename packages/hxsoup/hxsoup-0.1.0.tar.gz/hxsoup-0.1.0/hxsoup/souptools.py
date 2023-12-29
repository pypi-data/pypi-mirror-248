from __future__ import annotations
import typing
import contextlib

from httpx._models import Response
from typing import overload, Literal
from bs4 import BeautifulSoup
from bs4.element import Tag, ResultSet
from resoup.exceptions import EmptyResultError
from resoup.broadcast_list import TagBroadcastList

Parsers = Literal["html.parser", "html", "lxml", "lxml-xml", "xml", "html5lib", "html5"]


class SoupTools:
    def __init__(
        self,
        text: str,
        *,
        parser: Parsers | None = None,
        broadcasting: bool | None = None,
        no_empty_result: bool | None = None,
    ) -> None:
        with contextlib.suppress(AttributeError):
            # Response는 self.text를 덮어씌우도록 허락하지 않는다.
            self.text: str = text
        self.parser: Parsers | None = parser
        self.broadcasting = broadcasting
        self.no_empty_result = no_empty_result

    def _raise_error(
        self,
        error_message: str,
        selector: str,
        **kwargs,
    ) -> typing.NoReturn:
        raise EmptyResultError(error_message, selector=selector, **kwargs)

    def soup(
        self,
        parser: Parsers | None = None,
    ) -> BeautifulSoup:
        return BeautifulSoup(self.text, parser or self.parser or "html.parser")

    @overload
    def soup_select(
        self,
        selector: str,
        no_empty_result: bool = False,
        parser: Parsers | None = None,
        broadcasting: Literal[True] = ...,
    ) -> TagBroadcastList:
        ...

    @overload
    def soup_select(
        self,
        selector: str,
        no_empty_result: bool = False,
        parser: Parsers | None = None,
        broadcasting: Literal[False] = ...,
    ) -> ResultSet[Tag]:
        ...

    @overload
    def soup_select(
        self,
        selector: str,
        no_empty_result: bool = False,
        parser: Parsers | None = None,
        broadcasting: bool = False,
    ) -> ResultSet[Tag] | TagBroadcastList:
        ...

    def soup_select(
        self,
        selector: str,
        no_empty_result: bool = False,
        parser: Parsers | None = None,
        broadcasting: bool = False,
    ) -> ResultSet[Tag] | TagBroadcastList:
        """response.soup(parser, **kwargs).select(selector)와 거의 같습니다만 no_empty_result라는 강력한 추가 기능을 제공합니다.

        Args:
            self (str | Response): markup or response you want to parse.
            selector (str): BeatifulSoup.select의 selector입니다.
            no_empty_result (bool, optional): 결과가 빈 리스트라면 EmptyResultError를 냅니다. Defaults to False.
            parser (Parsers, optional): BeatifulSoup의 parser입니다. Defaults to 'html.parser'.

        Raises:
            EmptyResultError: 결과가 빈 리스트이고 no_empty_result가 참이라면 EmptyResultError를 냅니다.
                결과가 None일때 오류를 내는 것이 아니라는 점을 주의하세요.

        Returns:
            ResultSet[Tag]
        """
        selected = self.soup(parser).select(selector)
        if (no_empty_result or self.no_empty_result) and selected == []:
            self._raise_error(
                'Result of select is empty list("[]").',
                selector=selector,
            )

        return TagBroadcastList(selected) if broadcasting else selected

    @overload
    def soup_select_one(
        self,
        selector: str,
        no_empty_result: Literal[False] = ...,
        parser: Parsers | None = None,
    ) -> Tag | None:
        ...

    @overload
    def soup_select_one(
        self,
        selector: str,
        no_empty_result: Literal[True] = ...,
        parser: Parsers | None = None,
    ) -> Tag:
        ...

    @overload
    def soup_select_one(
        self,
        selector: str,
        no_empty_result: bool = False,
        parser: Parsers | None = None,
    ) -> Tag | None:
        ...

    def soup_select_one(
        self,
        selector: str,
        no_empty_result: bool = False,
        parser: Parsers | None = None,
    ) -> Tag | None:
        """response.soup(parser, **kwargs).select_one(selector)와 거의 같습니다만 no_empty_result라는 강력한 추가 기능을 제공합니다.

        Args:
            self (str | Response): markup or response you want to parse.
                (ResponesProxy에서 사용할 경우 없음)
            selector (str): BeatifulSoup.select_one의 selector입니다.
            no_empty_result (bool, optional): 결과(리턴값)가 None라면 EmptyResultError를 냅니다.
                typing과 오류 제거에 상당한 도움을 줍니다. 기존의 BeatifulSoup.select_one의 경우에는
                결과값이 None이거나 Tag였습니다. 따라서 BeatifulSoup.select_one(selector).text와 같은
                코드를 짤 때 정적 타입 검사기에서 오류를 내기 일쑤였고, 실제로 해당 코드 실행 결과가 None일 경우
                오류가 났습니다. no_empty_list를 이용해 불명확한 오류 대신 EmptyResultError를 내보내고
                타입 검사기의 오류도 피할 수 있어 좋은 기능입니다. 하지만 어떠한 이유로든지 이 기능을 사용하고
                싶지 않다면 간단히 그냥 값을 False로 하면 됩니다. Defaults to True.
            parser (Parsers, optional): BeatifulSoup의 parser입니다. Defaults to 'html.parser'.

        Raises:
            EmptyResultError: 결과가 None이고 no_empty_result가 참이라면 EmptyResultError를 냅니다.

        Returns:
            Tag | None: no_empty_result가 False일 경우(기본값)
            Tag: no_empty_result가 True일 경우(정적 검사기에 반영됨)
        """
        select_results = self.soup(parser).select_one(selector)
        if (no_empty_result or self.no_empty_result) and select_results is None:
            self._raise_error(
                'Result of select_one is None.',
                selector=selector,
            )

        return select_results

    # XML

    def xml(self) -> BeautifulSoup:
        """parser가 xml인 .soup()입니다. 자세한 내용은 .soup()의 docstring을 확인하세요."""
        # functools.partial을 사용할까도 했지만 그러면 type hint와 docstring 사용이 어렵다.
        return self.soup(parser='xml')

    @overload
    def xml_select(
        self,
        selector: str,
        no_empty_result: bool = False,
        use_broadcast_list: Literal[True] = ...,
    ) -> TagBroadcastList:
        ...

    @overload
    def xml_select(
        self,
        selector: str,
        no_empty_result: bool = False,
        use_broadcast_list: Literal[False] = ...,
    ) -> ResultSet[Tag]:
        ...

    @overload
    def xml_select(
        self,
        selector: str,
        no_empty_result: bool = False,
        use_broadcast_list: bool = True,
    ) -> ResultSet[Tag] | TagBroadcastList:
        ...

    def xml_select(
        self,
        selector: str,
        no_empty_result: bool = False,
        use_broadcast_list: bool = True,
    ) -> ResultSet[Tag] | TagBroadcastList:
        """parser가 xml인 .soup_select()입니다. 자세한 내용은 .soup_select()의 docstring을 확인하세요."""
        return self.soup_select(selector, no_empty_result, 'xml', use_broadcast_list)

    @overload
    def xml_select_one(
        self,
        selector: str,
        no_empty_result: Literal[True] = ...,
    ) -> Tag:
        ...

    @overload
    def xml_select_one(
        self,
        selector: str,
        no_empty_result: Literal[True] = ...,
    ) -> Tag:
        ...

    @overload
    def xml_select_one(
        self,
        selector: str,
        no_empty_result: bool = False,
    ) -> Tag | None:
        ...

    def xml_select_one(
        self,
        selector: str,
        no_empty_result: bool = False,
    ) -> Tag | None:
        """parser가 xml인 .soup_select_one()입니다. 자세한 내용은 .soup_select_one()의 docstring을 확인하세요."""
        return self.soup_select_one(selector, no_empty_result, 'xml')


class SoupedResponse(Response, SoupTools):
    def __init__(
        self,
        response: Response,
        *,
        parser: Parsers | None = None,
        broadcasting: bool | None = None,
        no_empty_result: bool | None = None,
    ) -> None:
        self.__dict__ = response.__dict__
        super(Response, self).__init__(
            response.text,
            parser=parser,
            broadcasting=broadcasting,
            no_empty_result=no_empty_result,
        )

    def _raise_error(self, *args, **kwargs):
        super()._raise_error(
            *args,
            **kwargs,
            url=self.url,
            status_code=self.status_code,
        )
