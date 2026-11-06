# Indic specialized token round-trip

Stock tokenizer decode of the stored uint16 span, with no special tokens added (`skip_special_tokens=False`), compared to the source text for the same uuid.
Each language uses the lexical first and last text parquet that already has both `.tokens.uint16` and `.tokens.index.jsonl`.
A language is omitted from the checks only when it has no finished token file.

| Language | File | Document | UUID | Result |
|---|---|---|---|---|
| bn-Beng-IN | bn-Beng-IN/Nemotron-Pretraining-Code-Concepts/train-00000-of-00777.parquet | first file, first document | 28a7db95-eed6-4c4b-9165-7fa54360c19e | mismatch at character 29 (source length 1088, decode length 1046): source 'mport List, Dict\n\ndef aggregate_amounts_' decode 'mport List, DictĊĊdef aggregate_amounts_' |
| bn-Beng-IN | bn-Beng-IN/Nemotron-Pretraining-Code-Concepts/train-00000-of-00777.parquet | first file, last document | af4be3b7-95b2-49c0-8b67-fd8553a3d2af | mismatch at character 23 (source length 1579, decode length 1493): source 'ping import List\n\ndef min_subarrays_cove' decode 'ping import ListĊĊdef min_subarrays_cove' |
| bn-Beng-IN | bn-Beng-IN/Nemotron-Pretraining-Wiki-Rewrite/train-00775-of-00777.parquet | last file, first document | afb60a6b-5090-46e1-99f6-14f3f0d5cb03 | mismatch at character 36 (source length 2501, decode length 2533): source 'ি সচেতনতা দিবস**\n\n**আন্তর্জাতিক তোতলামি ' decode 'ি সচেতনতা দিবস**ĊĊ **আন্তর্জাতিক তোতলামি' |
| bn-Beng-IN | bn-Beng-IN/Nemotron-Pretraining-Wiki-Rewrite/train-00775-of-00777.parquet | last file, last document | 616b3687-e5b5-44ca-b567-93acb5b64d7c | mismatch at character 8 (source length 3384, decode length 3426): source 'Ihringen\n\nIhringen জার্মানির Bad' decode 'IhringenĊĊIhringen জার্মানির Bad' |
| bn-Latn-IN | bn-Latn-IN/Nemotron-Pretraining-Code-Concepts/train-00018-of-00597.parquet | first file, first document | 12805a41-b1eb-4026-b870-f58d4d7b2936 | mismatch at character 29 (source length 1700, decode length 1610): source 'mport List, Dict\n\ndef filter_incomplete_' decode 'mport List, DictĊĊdef filter_incomplete_' |
| bn-Latn-IN | bn-Latn-IN/Nemotron-Pretraining-Code-Concepts/train-00018-of-00597.parquet | first file, last document | dfebc215-eedd-4d1c-a1cd-4ef9d8ebfc4b | mismatch at character 1106 (source length 2163, decode length 2163): source 'ore neya hocche – sorting GCD-ke probhab' decode 'ore neya hocche - sorting GCD-ke probhab' |
| bn-Latn-IN | bn-Latn-IN/Nemotron-Pretraining-Wiki-Rewrite/train-00303-of-00597.parquet | last file, first document | f49c9a9e-9200-4c38-b8d2-e093dd761d4f | mismatch at character 1196 (source length 3660, decode length 3660): source 'Fight Night One – Si Fight-e Lasnier Erm' decode 'Fight Night One - Si Fight-e Lasnier Erm' |
| bn-Latn-IN | bn-Latn-IN/Nemotron-Pretraining-Wiki-Rewrite/train-00303-of-00597.parquet | last file, last document | 45419774-0d39-48f7-a241-5ecf93cfddff | mismatch at character 328 (source length 988, decode length 988): source 'FC Homburg (1988–1991): 23ti match, 2 go' decode 'FC Homburg (1988-1991): 23ti match, 2 go' |
| gu-Gujr-IN | gu-Gujr-IN/Nemotron-Pretraining-Code-Concepts/train-00017-of-06052.parquet | first file, first document | 3078681e-b482-41a8-8c51-d6f401d194be | mismatch at character 37 (source length 1808, decode length 1663): source 'st, Tuple, Union\n\ndef parse_and_sum(valu' decode 'st, Tuple, UnionĊĊdef parse_and_sum(valu' |
| gu-Gujr-IN | gu-Gujr-IN/Nemotron-Pretraining-Code-Concepts/train-00017-of-06052.parquet | first file, last document | a368801d-a4b3-4d9c-9695-e6ece988e738 | mismatch at character 23 (source length 2143, decode length 1993): source 'ping import List\n\ndef balance_parenthese' decode 'ping import ListĊĊdef balance_parenthese' |
| gu-Gujr-IN | gu-Gujr-IN/Nemotron-Pretraining-Wiki-Rewrite/train-06029-of-06052.parquet | last file, first document | 1e65ee1e-5d83-4fdc-a6be-e05cdc1f69fb | mismatch at character 35 (source length 4496, decode length 4538): source 'e Changelings)**\n\n*ધ ચેન્જલિંગ્સ* એ જો સ' decode 'e Changelings)**ĊĊ *ધ ચેન્જલિંગ્સ* એ જો ' |
| gu-Gujr-IN | gu-Gujr-IN/Nemotron-Pretraining-Wiki-Rewrite/train-06029-of-06052.parquet | last file, last document | 011e69fd-a195-4d85-9727-458d0578f846 | mismatch at character 45 (source length 1551, decode length 1558): source 'ટ બાસ્કેટબોલ લીગ\n\nઇસ્ટર્ન પેન્સિલવેનિયા ' decode 'ટ બાસ્કેટબોલ લીગĊĊ ઇસ્ટર્ન પેન્સિલવેનિયા' |
| gu-Latn-IN | gu-Latn-IN/Nemotron-Pretraining-Code-Concepts/train-00024-of-00560.parquet | first file, first document | f5f1ef59-b47d-4b6c-b5ac-c075c95f9980 | mismatch at character 30 (source length 1945, decode length 1796): source 'port List, Tuple\n\ndef count_prime_letter' decode 'port List, TupleĊĊdef count_prime_letter' |
| gu-Latn-IN | gu-Latn-IN/Nemotron-Pretraining-Code-Concepts/train-00024-of-00560.parquet | first file, last document | f8ace699-e7da-4275-9034-5a2d424fbe11 | match |
| gu-Latn-IN | gu-Latn-IN/Nemotron-Pretraining-Wiki-Rewrite/train-00179-of-00560.parquet | last file, first document | 7500c7ea-c2f4-44ab-a065-c1c99f87d347 | match |
| gu-Latn-IN | gu-Latn-IN/Nemotron-Pretraining-Wiki-Rewrite/train-00179-of-00560.parquet | last file, last document | c0f2e643-f685-4abe-af93-dde848d6c8b4 | match |
| hi-Deva-IN | hi-Deva-IN/Nemotron-Pretraining-Code-Concepts/train-00040-of-05658.parquet | first file, first document | 439e91a8-93a8-449a-8279-afd23dd7a65b | mismatch at character 30 (source length 1925, decode length 1789): source 'port List, Union\n\ndef search_rounded_sub' decode 'port List, UnionĊĊdef search_rounded_sub' |
| hi-Deva-IN | hi-Deva-IN/Nemotron-Pretraining-Code-Concepts/train-00040-of-05658.parquet | first file, last document | 1786c637-2e6c-4a96-9660-627fdedaded2 | mismatch at character 30 (source length 1531, decode length 1425): source 'port List, Tuple\n\ndef find_palindromic_t' decode 'port List, TupleĊĊdef find_palindromic_t' |
| hi-Deva-IN | hi-Deva-IN/Nemotron-Pretraining-Wiki-Rewrite/train-05568-of-05658.parquet | last file, first document | bfe1e0b0-b57c-415d-b8aa-5e2f60002499 | mismatch at character 48 (source length 400, decode length 401): source 'त से हो सकता है:\n\n* Francis Dana (1743–1' decode 'त से हो सकता है:ĊĊ* Francis Dana (1743-1' |
| hi-Deva-IN | hi-Deva-IN/Nemotron-Pretraining-Wiki-Rewrite/train-05568-of-05658.parquet | last file, last document | 17576a7b-30c3-4664-b8b8-5f08f64693ec | mismatch at character 5 (source length 1442, decode length 1444): source 'Co La\n\n\| जन्म का नाम \| Matthe' decode 'Co LaĊĊ \| जन्म का नाम \| Matth' |
| hi-Latn-IN | hi-Latn-IN/Nemotron-Pretraining-Code-Concepts/train-00008-of-00570.parquet | first file, first document | 4440788d-80f8-42f6-9ee7-6eab06fc7f6f | match |
| hi-Latn-IN | hi-Latn-IN/Nemotron-Pretraining-Code-Concepts/train-00008-of-00570.parquet | first file, last document | 08511a26-088b-4e92-810c-b74f1bdc58e0 | match |
| hi-Latn-IN | hi-Latn-IN/Nemotron-Pretraining-Wiki-Rewrite/train-00209-of-00570.parquet | last file, first document | 89962090-3e06-462c-81d6-d8a8f226e0df | mismatch at character 2446 (source length 9636, decode length 9636): source 'London) .885 (23–3)  \n- Home Run: chaar ' decode 'London) .885 (23-3)  \n- Home Run: chaar ' |
| hi-Latn-IN | hi-Latn-IN/Nemotron-Pretraining-Wiki-Rewrite/train-00209-of-00570.parquet | last file, last document | ba90560d-184d-4c6c-959e-263f655fd859 | mismatch at character 20 (source length 1125, decode length 1125): source 'd Barclay (1823 – 10 September, 1889) Pe' decode 'd Barclay (1823 - 10 September, 1889) Pe' |
| kn-Knda-IN | kn-Knda-IN/Nemotron-Pretraining-Code-Concepts/train-00011-of-07065.parquet | first file, first document | a076f211-fd8b-4767-93d9-63157f5669d1 | mismatch at character 23 (source length 1307, decode length 1208): source 'ping import List\n\ndef longest_zero_mod_s' decode 'ping import ListĊĊdef longest_zero_mod_s' |
| kn-Knda-IN | kn-Knda-IN/Nemotron-Pretraining-Code-Concepts/train-00011-of-07065.parquet | first file, last document | 259f207b-ab4a-4261-9d60-230a5b937a17 | mismatch at character 22 (source length 1357, decode length 1257): source 'yping import Set\n\ndef count_valid_word_p' decode 'yping import SetĊĊdef count_valid_word_p' |
| kn-Knda-IN | kn-Knda-IN/Nemotron-Pretraining-Wiki-Rewrite/train-06877-of-07065.parquet | last file, first document | 4457c44a-c116-40f1-9174-a6f5ae7c029e | mismatch at character 10 (source length 3519, decode length 3494): source 'Candee Jay\n\n\|  \| ಜೀವಂತ ವ್ಯಕ್ತಿಯ ಈ ' decode 'Candee JayĊĊ \| \| ಜೀವಂತ ವ್ಯಕ್ತಿಯ ಈ ' |
| kn-Knda-IN | kn-Knda-IN/Nemotron-Pretraining-Wiki-Rewrite/train-06877-of-07065.parquet | last file, last document | 91f7cf43-8ff3-48e4-9142-fdeb365457da | mismatch at character 372 (source length 12276, decode length 12332): source 'ನಿರ್ವಹಿಸುತ್ತಾರೆ.\n\n\| ಸದಸ್ಯರು \| ಡিয়েಗೋ ಬಾ' decode 'ನಿರ್ವಹಿಸುತ್ತಾರೆ.ĊĊ \| ಸದಸ್ಯರು \| ಡিয়েಗೋ ಬ' |
| kn-Latn-IN | kn-Latn-IN/Nemotron-Pretraining-Economics/train-00115-of-01126.parquet | first file, first document | cd1a8dc9-4939-4773-b561-8c29d218a2d3 | match |
| kn-Latn-IN | kn-Latn-IN/Nemotron-Pretraining-Economics/train-00115-of-01126.parquet | first file, last document | 281f95a2-95a5-41f5-b635-cf0bdf36e02c | match |
| kn-Latn-IN | kn-Latn-IN/Nemotron-Pretraining-Wiki-Rewrite/train-00336-of-01126.parquet | last file, first document | 295c89f5-35f3-458e-ae4c-69d06e7fb2f9 | mismatch at character 1712 (source length 1751, decode length 1751): source 'rdeshankagalu\n25°15′00″N 87°02′00″E / 25' decode 'rdeshankagalu\n25�15\'00"N 87�02\'00"E / 25' |
| kn-Latn-IN | kn-Latn-IN/Nemotron-Pretraining-Wiki-Rewrite/train-00336-of-01126.parquet | last file, last document | df4a2f68-e8e7-4cc7-b4e6-1dab8ea70d91 | mismatch at character 116 (source length 469, decode length 469): source 'u 1927 ralli René Jeannel avaru vivarisi' decode 'u 1927 ralli Ren� Jeannel avaru vivarisi' |
| mr-Deva-IN | mr-Deva-IN/Nemotron-Pretraining-Code-Concepts/train-00069-of-05692.parquet | first file, first document | a91a3307-ce5f-4160-a00f-49f44495fdb9 | mismatch at character 29 (source length 1878, decode length 1737): source 'mport List, Dict\n\ndef max_unique_char_di' decode 'mport List, DictĊĊdef max_unique_char_di' |
| mr-Deva-IN | mr-Deva-IN/Nemotron-Pretraining-Code-Concepts/train-00069-of-05692.parquet | first file, last document | c1de06fc-4db7-474f-83f5-d71925f617d2 | mismatch at character 36 (source length 4782, decode length 4297): source 'ict, List, Tuple\n\ndef find_prime_weighte' decode 'ict, List, TupleĊĊdef find_prime_weighte' |
| mr-Deva-IN | mr-Deva-IN/Nemotron-Pretraining-Unconditional-Algorithmic/train-05462-of-05692.parquet | last file, first document | e0219b23-a4c7-454f-8834-225832cb1db9 | mismatch at character 11 (source length 6585, decode length 6237): source '**Problem**\n\nतुम्हाला `N` व्हर्टिसे' decode '**Problem**ĊĊ तुम्हाला `N` व्हर्टिस' |
| mr-Deva-IN | mr-Deva-IN/Nemotron-Pretraining-Unconditional-Algorithmic/train-05462-of-05692.parquet | last file, last document | 12212efe-a1ad-41e6-a099-991b1888c85a | mismatch at character 71 (source length 4399, decode length 4253): source 'ictly Increasing\n\nतुम्हाला `N` पूर्णांका' decode 'ictly IncreasingĊĊ तुम्हाला `N` पूर्णांक' |
| mr-Latn-IN | mr-Latn-IN/Nemotron-Pretraining-Code-Concepts/train-00058-of-00657.parquet | first file, first document | c2b973fe-5cff-487c-9bf3-d4d1152ea238 | match |
| mr-Latn-IN | mr-Latn-IN/Nemotron-Pretraining-Code-Concepts/train-00058-of-00657.parquet | first file, last document | 9138d616-30a9-4323-844b-8dbc7cd7b37b | match |
| mr-Latn-IN | mr-Latn-IN/Nemotron-Pretraining-Wiki-Rewrite/train-00249-of-00657.parquet | last file, first document | 281a6a75-4685-4c91-90d4-d417247f66d8 | mismatch at character 467 (source length 826, decode length 826): source 'ios Korais (1748–1833), manavtavadi vidv' decode 'ios Korais (1748-1833), manavtavadi vidv' |
| mr-Latn-IN | mr-Latn-IN/Nemotron-Pretraining-Wiki-Rewrite/train-00249-of-00657.parquet | last file, last document | 7097b9dc-be27-4ffa-b907-780c801b25bc | mismatch at character 637 (source length 2064, decode length 2064): source ', jyachi lambi 6–20 mm ani rundi sumare ' decode ', jyachi lambi 6-20 mm ani rundi sumare ' |
| ta-Latn-IN | ta-Latn-IN/Nemotron-Pretraining-Code-Concepts/train-00020-of-01160.parquet | first file, first document | f61b47b8-ab6b-47a1-8a4c-a6c4bea4e35e | match |
| ta-Latn-IN | ta-Latn-IN/Nemotron-Pretraining-Code-Concepts/train-00020-of-01160.parquet | first file, last document | f714333b-df01-41fc-9398-3bb8735c09ea | match |
| ta-Latn-IN | ta-Latn-IN/Nemotron-Pretraining-Unconditional-Algorithmic/train-00124-of-01160.parquet | last file, first document | fb66a751-5a19-4ced-99f9-4f29ca09114d | mismatch at character 127 (source length 8222, decode length 7909): source 'mall Patterns)**\n\nUngalukku aangila siri' decode 'mall Patterns)**ĊĊUngalukku aangila siri' |
| ta-Latn-IN | ta-Latn-IN/Nemotron-Pretraining-Unconditional-Algorithmic/train-00124-of-01160.parquet | last file, last document | 86eccd2b-b7c7-463a-93db-241b10d81909 | mismatch at character 9 (source length 4685, decode length 4561): source 'Prachinai\n-------\n**Minimum Cost ' decode 'PrachinaiĊ-------Ċ**Minimum Cost ' |
| ta-Taml-IN | ta-Taml-IN/Nemotron-Pretraining-Code-Concepts/train-00000-of-00779.parquet | first file, first document | 42a32cbf-3adb-4142-b5bb-d090c4e70857 | mismatch at character 30 (source length 1502, decode length 1411): source 'port List, Tuple\n\ndef count_reachable_su' decode 'port List, TupleĊĊdef count_reachable_su' |
| ta-Taml-IN | ta-Taml-IN/Nemotron-Pretraining-Code-Concepts/train-00000-of-00779.parquet | first file, last document | 354f9ce1-3fcd-4a08-b59f-3f936762f308 | mismatch at character 30 (source length 2897, decode length 2666): source 'port List, Tuple\n\ndef normalize_and_thre' decode 'port List, TupleĊĊdef normalize_and_thre' |
| ta-Taml-IN | ta-Taml-IN/Nemotron-Pretraining-STEM-SFT/train-00236-of-00779.parquet | last file, first document | c5d52caa-6d7e-4733-b76a-61e4d49faf81 | mismatch at character 247 (source length 6949, decode length 6971): source '** கால அளவு எது?\n\nA: 5 வினாடிகளுக்கு மேல' decode '** கால அளவு எது?ĊĊA: 5 வினாடிகளுக்கு மேல' |
| ta-Taml-IN | ta-Taml-IN/Nemotron-Pretraining-STEM-SFT/train-00236-of-00779.parquet | last file, last document | a8f4e20b-1ae8-4a6e-870e-1d24ba7f257f | mismatch at character 317 (source length 15947, decode length 16074): source 'lute position P-யையும், யுனிவர்ஸ் Y என்ப' decode 'lute position P- யையும், யுனிவர்ஸ் Y என்' |
| te-Latn-IN | te-Latn-IN/Nemotron-Pretraining-Formal-Logic/train-00075-of-01099.parquet | first file, first document | db5df226-8c85-431d-b0f7-e18688d8ec59 | match |
| te-Latn-IN | te-Latn-IN/Nemotron-Pretraining-Formal-Logic/train-00075-of-01099.parquet | first file, last document | 271945e5-e9da-4888-9029-b417ea8da580 | mismatch at character 179 (source length 303, decode length 303): source 'ni ngurshistaru)\nA. (∀x)(Ex → (∃y)(Ax → ' decode 'ni ngurshistaru)ĊA. (∀x)(Ex → (∃y)(Ax → ' |
| te-Latn-IN | te-Latn-IN/Nemotron-Pretraining-Unconditional-Algorithmic/train-00109-of-01099.parquet | last file, first document | 3fe15e32-0496-4e99-9a6f-886e7c4b1545 | mismatch at character 11 (source length 7168, decode length 6794): source '**Samasya**\n\nMeeku `N` poornankalat' decode '**Samasya**ĊĊMeeku `N` poornankalat' |
| te-Latn-IN | te-Latn-IN/Nemotron-Pretraining-Unconditional-Algorithmic/train-00109-of-01099.parquet | last file, last document | 44bb8a4c-2b1d-423d-956b-77c7abe3c6d6 | mismatch at character 57 (source length 1077, decode length 999): source 's2: str) -> int:\n    """\n    Rendu strin' decode 's2: str) -> int:Ċ  """Ċ  Rendu strings y' |
| te-Telu-IN | te-Telu-IN/Nemotron-Pretraining-Formal-Logic/train-00597-of-06169.parquet | first file, first document | cadc1639-112d-49e6-8a78-fe5d38f463e1 | mismatch at character 87 (source length 791, decode length 792): source 'వరణను ఎంచుకోండి:\n(∀x)[(Ex • Rx) ⊃ Lx]\nEk' decode 'వరణను ఎంచుకోండి:Ċ(∀x)[(Ex • Rx) ⊃ Lx]ĊEk' |
| te-Telu-IN | te-Telu-IN/Nemotron-Pretraining-Formal-Logic/train-00597-of-06169.parquet | first file, last document | f33522c0-037f-47db-b9c9-72ae7db8ad13 | mismatch at character 84 (source length 984, decode length 986): source 'వరణను ఎంచుకోండి:\n(∀x)[Hx ⊃ ¬Rx]\n(∃x)(Hx ' decode 'వరణను ఎంచుకోండి:Ċ(∀x)[Hx ⊃ ¬Rx]Ċ(∃x)(Hx ' |
| te-Telu-IN | te-Telu-IN/Nemotron-Pretraining-Wiki-Rewrite/train-04928-of-06169.parquet | last file, first document | 2e15797a-c736-48e3-ba2b-619d431f36f8 | mismatch at character 16 (source length 5095, decode length 5108): source '**Centrepointe**\n\nCentrepointe అనేది కెన' decode '**Centrepointe**ĊĊCentrepointe అనేది కెన' |
| te-Telu-IN | te-Telu-IN/Nemotron-Pretraining-Wiki-Rewrite/train-04928-of-06169.parquet | last file, last document | ebed1016-76a7-438e-8cd8-bd59cfe69aa5 | mismatch at character 124 (source length 865, decode length 869): source 'ally కప్\u200c విజేత.\n\n## కెరీర్\n\nమిఖల్ జ్డార' decode 'ally కప్\u200c విజేత.ĊĊ ## కెరీర్ĊĊ మిఖల్ జ్డ' |

## Stored ids versus stock encode

Same 56 documents. Stored little-endian uint16 ids compared with `Tokenizer.encode(source text, add_special_tokens=False).ids` on the stock tokenizer.
Stock ids were decoded with `decode(..., skip_special_tokens=False)`, the same call used for the stored span.
`stock_decode_same_diff` is yes when that stock decode string equals the stored-id decode, so the newline-to-Ċ and en-dash-to-hyphen changes are the stock tokenizer's own decode.

| Language | Document | ids_match | stock_decode_same_diff |
|---|---|---|---|
| bn-Beng-IN | first file, first document | yes | yes |
| bn-Beng-IN | first file, last document | yes | yes |
| bn-Beng-IN | last file, first document | yes | yes |
| bn-Beng-IN | last file, last document | yes | yes |
| bn-Latn-IN | first file, first document | yes | yes |
| bn-Latn-IN | first file, last document | yes | yes |
| bn-Latn-IN | last file, first document | yes | yes |
| bn-Latn-IN | last file, last document | yes | yes |
| gu-Gujr-IN | first file, first document | yes | yes |
| gu-Gujr-IN | first file, last document | yes | yes |
| gu-Gujr-IN | last file, first document | yes | yes |
| gu-Gujr-IN | last file, last document | yes | yes |
| gu-Latn-IN | first file, first document | yes | yes |
| gu-Latn-IN | first file, last document | yes | yes |
| gu-Latn-IN | last file, first document | yes | yes |
| gu-Latn-IN | last file, last document | yes | yes |
| hi-Deva-IN | first file, first document | yes | yes |
| hi-Deva-IN | first file, last document | yes | yes |
| hi-Deva-IN | last file, first document | yes | yes |
| hi-Deva-IN | last file, last document | yes | yes |
| hi-Latn-IN | first file, first document | yes | yes |
| hi-Latn-IN | first file, last document | yes | yes |
| hi-Latn-IN | last file, first document | yes | yes |
| hi-Latn-IN | last file, last document | yes | yes |
| kn-Knda-IN | first file, first document | yes | yes |
| kn-Knda-IN | first file, last document | yes | yes |
| kn-Knda-IN | last file, first document | yes | yes |
| kn-Knda-IN | last file, last document | yes | yes |
| kn-Latn-IN | first file, first document | yes | yes |
| kn-Latn-IN | first file, last document | yes | yes |
| kn-Latn-IN | last file, first document | yes | yes |
| kn-Latn-IN | last file, last document | yes | yes |
| mr-Deva-IN | first file, first document | yes | yes |
| mr-Deva-IN | first file, last document | yes | yes |
| mr-Deva-IN | last file, first document | yes | yes |
| mr-Deva-IN | last file, last document | yes | yes |
| mr-Latn-IN | first file, first document | yes | yes |
| mr-Latn-IN | first file, last document | yes | yes |
| mr-Latn-IN | last file, first document | yes | yes |
| mr-Latn-IN | last file, last document | yes | yes |
| ta-Latn-IN | first file, first document | yes | yes |
| ta-Latn-IN | first file, last document | yes | yes |
| ta-Latn-IN | last file, first document | yes | yes |
| ta-Latn-IN | last file, last document | yes | yes |
| ta-Taml-IN | first file, first document | yes | yes |
| ta-Taml-IN | first file, last document | yes | yes |
| ta-Taml-IN | last file, first document | yes | yes |
| ta-Taml-IN | last file, last document | yes | yes |
| te-Latn-IN | first file, first document | yes | yes |
| te-Latn-IN | first file, last document | yes | yes |
| te-Latn-IN | last file, first document | yes | yes |
| te-Latn-IN | last file, last document | yes | yes |
| te-Telu-IN | first file, first document | yes | yes |
| te-Telu-IN | first file, last document | yes | yes |
| te-Telu-IN | last file, first document | yes | yes |
| te-Telu-IN | last file, last document | yes | yes |

56 of 56 documents have identical ids. 56 of 56 have the same decode string as the stored ids.
