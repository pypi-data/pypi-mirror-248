import click
from pathlib import Path


def is_startswith_end_parenthesis(text: str) -> bool:
    """
    カッコ閉じで始まっているかどうか

    例:
    - "」テスト" は True
    - ")テスト" は True
    """
    return text.startswith("」") or text.startswith(")") or text.startswith("）")


def is_markdown_title(text: str) -> bool:
    """
    マークダウンのタイトルかどうか

    例:
    - "# テスト" は True
    - "## テスト" は True
    """
    return (
        text.startswith("# ")
        or text.startswith("## ")
        or text.startswith("### ")
        or text.startswith("#### ")
        or text.startswith("##### ")
        or text.startswith("###### ")
    )


def is_markdonw_item(text: str) -> bool:
    """
    マークダウンの箇条書きかどうか

    例:
    - "- テスト" は True
    - "+ テスト" は True
    - "* テスト" は True
    """
    return text.startswith("- ") or text.startswith("+ ") or text.startswith("* ")


def insert_newline_after_period(text: str) -> str:
    """
    「。」の後に改行を入れる
    """

    # リストの場合は、改行を入れないようにする
    lines = text.split("\n")
    for index, line in enumerate(lines):
        if is_markdonw_item(line):
            lines[index] = line.replace("。", "<escape>")

    text = "\n".join(lines)

    segments = text.split("。")
    for index, segment in enumerate(segments):
        if index == len(segments) - 1:
            break

        next_segment = segments[index + 1] if index + 1 < len(segments) else ""

        if not next_segment.startswith("\n") and not is_startswith_end_parenthesis(
            next_segment
        ):
            result_segment = segment + "。\n"
        else:
            result_segment = segment + "。"

        segments[index] = result_segment

    text = "".join(segments)

    # リストの場合は、改行を入れないようにする
    text = text.replace("<escape>", "。")

    return text


def normalize_end_period(text: str) -> str:
    """
    文末に必ず「。」をつける

    ただし、以下のケースは除く

    - 空行
    - マークダウンのタイトル
    """
    segments = text.split("\n")

    for index, segment in enumerate(segments):
        result_segment = segment

        if segment == "":
            continue
        if is_markdown_title(segment):
            continue
        if is_markdonw_item(segment):
            continue
        if segment.endswith("。"):
            result_segment = segment
        else:
            result_segment = segment + "。"

        segments[index] = result_segment

    text = "\n".join(segments)
    return text


@click.command()
@click.argument("filepath")
def toishi(filepath: str):
    """
    指定されたファイルをフォーマットする
    """
    filepath = Path(filepath)
    filetext = filepath.read_text(encoding="utf-8")

    # 「。」の後に改行を入れる
    filetext = insert_newline_after_period(filetext)

    # 文末に必ず「。」をつける
    filetext = normalize_end_period(filetext)

    filepath.write_text(filetext, encoding="utf-8")
    click.echo("Done!")


if __name__ == "__main__":
    toishi()
