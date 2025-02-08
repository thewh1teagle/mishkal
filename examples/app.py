"""
uv venv
uv pip install -e .
uv run examples/app.py
"""

from mishkal.g2p import text_to_ipa
import gradio as gr

default_text = """
כָּל עֶרֶב יָאִיר (הַשֵּׁם הַמָּלֵא וּמְקוֹם הָעֲבוֹדָה שֶׁלּוֹ שְׁמוּרִים בַּמַּעֲרֶכֶת) רָץ 20 קִילוֹמֶטֶר. הוּא מְסַפֵּר לִי שֶׁזֶּה מְנַקֶּה לוֹ אֶת הָרֹאשׁ אַחֲרֵי הָעֲבוֹדָה, "שָׁעָה וָחֵצִי בְּלִי עֲבוֹדָה, אִשָּׁה וִילָדִים" כְּמוֹ שֶׁהוּא מַגְדִּיר זֹאת. אֲבָל אַחֲרֵי הַמִּקְלַחַת הוּא מַתְחִיל בְּמָה שֶׁנִּתָּן לְכַנּוֹת הָעֲבוֹדָה הַשְּׁנִיָּה שֶׁלּוֹ: לִמְצֹא לוֹ קוֹלֵגוֹת חֲדָשׁוֹת לָעֲבוֹדָה, כִּי יָאִיר הוּא כַּנִּרְאֶה הַמֶּלֶךְ שֶׁל "חָבֵר מֵבִיא חָבֵר" בְּיִשְׂרָאֵל.
"""

ui = gr.Interface(
    fn=text_to_ipa,
    inputs=gr.Textbox(value=default_text, label="Input Text", rtl=True),
    outputs="text",
    title="Text to IPA Converter",
    description="Enter Hebrew text and get the IPA transcription.",
)

# Launch the app
ui.launch()
