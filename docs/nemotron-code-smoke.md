# Nemotron Code v2 tokenizer smoke

`aws sts get-caller-identity` succeeded for the historical research account.

| | |
| --- | ---: |
| Documents read | 301 |
| Total tokens | 335,798 |
| Tokens per document | 1,115.6 mean (min 123, median 961, max 3,816) |
| UTF-8 bytes | 1,063,693 |
| Bytes per token | 3.168 |

S3 key: `s3://<research-data-bucket>/datasets/nemotron-code-v2/synthetic-code-review/part_00005.parquet` (region `us-east-1`). Object size 2,389,554,160 bytes, 1,336,018 rows, 18 row groups. These 301 documents are the first data page of row group 0 (compressed page 500,184 bytes, starting at file offset 4). No other object under the prefix was read.

Column `content`. Languages in these 301 rows: Python 228, C++ 73. `seed_source`: Nemotron-Pretraining-Code-v1 210, Nemotron-Pretraining-Code-v2 91. Row order matches `language`, `seed_source`, and `nemotron_pretraining_id`.

Encoder: `tokenizers.Tokenizer.from_file` on `docs/hf-tokenizer/tokenizer.json`. `encode(..., add_special_tokens=False)`. `<eod>` was not appended.

Every content id from these 301 documents was checked.

| Check | Result |
| --- | --- |
| Ids outside 0–65535 | 0 |
| Ids in 0–31 | 0 |
| `<eod>` (id 4) | 0 |

Ids 0–31 in this file are `<unk>`, `<s>`, `</s>`, `<pad>`, `<eod>`, and `<reserved_0005>` through `<reserved_0031>`. None of them occur in this page.

## Samples

Each block is a contiguous slice of one document, cut on line boundaries. The raw text is unchanged. The split is that slice only, not the rest of the document. Pieces are the tokenizer strings, separated by ` | `. `▁` is `Ġ` (a leading space), `↵` is `Ċ` (newline), `⇥` is `ĉ` (tab), `␍` is `č` (carriage return). `<0xHH>` is a byte-fallback piece.

### 1. Ordinary Python

Row 38 (0-based in this shard), lines 6–15. Python. `Nemotron-Pretraining-Code-v1`. `a6fec7ef-8430-4f9d-b6d2-9f5a8419d556`.

A turtle drawing loop. The quotes are short prompts. Excerpt: **73** tokens. Whole document: 275 tokens, 890 bytes.

```
def main():
    while True:
        try:
            side = float(input('Enter a side length: '))
            if side <= 0:
                print("Please enter a positive number")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a numeric value")
```

```
def | ▁main | () | : | ↵▁ | ▁▁ | ▁while | ▁True | : | ↵▁ | ▁▁▁▁▁▁ | ▁try
: | ↵▁▁▁▁▁▁▁▁▁ | ▁▁ | ▁side | ▁ | = | ▁float | (in | put | (' | Enter | ▁a
▁side | ▁length | : | ▁ | ' | )) | ↵▁▁▁▁▁▁▁▁▁▁▁▁ | if | ▁side | ▁ | <= | ▁
0 | : | ↵▁▁▁▁▁▁▁▁▁ | ▁▁▁▁▁▁ | ▁print | (" | Please | ▁enter | ▁a | ▁positive | ▁number | ")
↵▁▁▁▁▁▁▁▁▁ | ▁▁▁▁▁▁ | ▁continue | ↵▁▁▁▁▁▁▁▁▁ | ▁▁ | ▁break | ↵▁ | ▁▁▁▁▁▁▁ | except | ▁ValueError | : | ↵▁▁▁▁▁▁▁▁▁
▁▁ | ▁print | (" | Invalid | ▁input | . | ▁Please | ▁enter | ▁a | ▁numeric | ▁value | ")
↵
```

### 2. Ordinary Python

Row 9 (0-based in this shard), lines 12–22. Python. `Nemotron-Pretraining-Code-v1`. `7ef26cce-178a-4455-aa8d-b9036d546206`.

Game entry point: a docstring, a comment, and a state dictionary. Excerpt: **125** tokens. Whole document: 329 tokens, 1092 bytes.

```
def main():
    """Start the game engine with state machines."""
    try:
        game = tool.Control()
        # Using factory pattern for lazy initialization
        state_dict = {
            c.MAIN_MENU: mainmenu.Menu,
            c.GAME_VICTORY: screen.GameVictoryScreen,
            c.GAME_LOSE: screen.GameLoseScreen,
            c.LEVEL: level.Level
        }
```

```
def | ▁main | () | : | ↵▁ | ▁▁▁ | "" | " | Start | ▁the | ▁game | ▁engine
▁with | ▁state | ▁machines | ." | "" | ↵▁ | ▁▁ | ▁try | : | ↵▁ | ▁▁▁▁▁▁▁ | g
ame | ▁ | = | ▁tool | . | Cont | rol | () | ↵▁ | ▁▁▁▁▁▁▁ | # | ▁Using
▁factory | ▁pattern | ▁for | ▁lazy | ▁initial | ization | ↵▁ | ▁▁▁▁▁▁ | ▁state | _dict | ▁ | =
▁ | { | ↵▁▁▁▁▁▁▁▁▁ | ▁▁ | ▁c | . | MA | IN | _M | EN | U | :
▁main | men | u | .M | en | u | , | ↵▁▁▁▁▁▁▁▁▁ | ▁▁ | ▁c | . | G
AM | E | _V | IC | T | ORY | : | ▁screen | . | G | ame | V
ict | ory | S | creen | , | ↵▁▁▁▁▁▁▁▁▁ | ▁▁ | ▁c | . | G | AM | E
_L | O | SE | : | ▁screen | . | G | ame | L | ose | S | creen
, | ↵▁▁▁▁▁▁▁▁▁ | ▁▁ | ▁c | . | LE | V | EL | : | ▁level | . | Le
vel | ↵▁ | ▁▁▁▁▁▁▁ | } | ↵
```

### 3. Ordinary C++

Row 18 (0-based in this shard), lines 3–14. C++. `Nemotron-Pretraining-Code-v1`. `3a3e00df-b121-49b0-b007-3141f754462a`.

Includes, a namespace, and a constructor. The indented lines are tabs. Excerpt: **101** tokens. Whole document: 564 tokens, 1451 bytes.

```
#include "App.h"
#include "Director.h"
#include <memory>

namespace z {

App* GApp = nullptr;

App::App() : mInput(nullptr), mDirector(nullptr) {
	InitializeSingleton<App>(GApp, this);
	mEnableEditorUI = false;
}
```

```
# | in | clude | ▁ | " | App | .h | " | ↵ | # | in | clude
▁ | "D | ire | ctor | .h | " | ↵ | # | in | clude | ▁ | <
m | em | ory | > | ↵ | ↵ | n | ames | pace | ▁z | ▁ | {
↵ | ↵ | App | * | ▁G | App | ▁ | = | ▁null | pt | r | ;
↵ | ↵ | App | :: | App | () | ▁ | : | ▁m | Input | (n | ull
pt | r | ), | ▁m | D | ire | ctor | (n | ull | pt | r | )
▁ | { | ↵⇥ | Initialize | S | ingle | ton | < | App | >( | G | App
, | ▁this | ); | ↵⇥ | m | En | able | Ed | itor | UI | ▁ | =
▁false | ; | ↵ | } | ↵
```

### 4. Ordinary C++

Row 7 (0-based in this shard), lines 17–26. C++. `Nemotron-Pretraining-Code-v1`. `8968a5dc-6ee5-4489-9158-25873831dd13`.

A stack unit test. The asserts mix a call, a comparison, and a string. Excerpt: **118** tokens. Whole document: 1757 tokens, 4157 bytes.

```
bool StackInit()
{
    MemoryArena arena = {};
    uint32 testSize = 10;

    Stack s = {};
    s.Init(testSize);

    if (!_Assert(s.items != NULL, "s.items != NULL")) return false;
    if (!_Assert(s.size == testSize, "s.size == %d", testSize)) return false;
```

```
bool | ▁Stack | In | it | () | ↵ | { | ↵▁ | ▁▁▁ | M | em | ory
A | ren | a | ▁are | na | ▁ | = | ▁ | { | }; | ↵▁ | ▁▁▁
u | int | 3 | 2 | ▁test | Size | ▁ | = | ▁ | 1 | 0 | ;
↵ | ↵▁ | ▁▁▁ | St | ack | ▁s | ▁ | = | ▁ | { | }; | ↵▁
▁▁ | ▁s | .In | it | (t | est | Size | ); | ↵ | ↵▁ | ▁▁▁ | if
▁ | (! | _ | Ass | ert | (s | .items | ▁ | != | ▁N | U | LL
, | ▁ | "s | .items | ▁ | != | ▁N | U | LL | ")) | ▁return | ▁false
; | ↵▁ | ▁▁▁ | if | ▁ | (! | _ | Ass | ert | (s | .s | ize
▁ | == | ▁test | Size | , | ▁ | "s | .s | ize | ▁ | == | ▁
% | d | ", | ▁test | Size | )) | ▁return | ▁false | ; | ↵
```

### 5. Comment-heavy C++

Row 32 (0-based in this shard), lines 14–20. C++. `Nemotron-Pretraining-Code-v1`. `dbda776b-834c-490a-84b8-1237206ddc82`.

Irrlicht driver enum. The comments here are `//!` lines and one `/** */` block. Excerpt: **91** tokens. Whole document: 705 tokens, 2572 bytes.

```
        //! An enum for all types of drivers the Irrlicht Engine supports.  
        enum E_DRIVER_TYPE  
        {  
            //! Null driver, useful for applications to run the engine without visualisation.  
            /** The null device is able to load textures, but does not  
            render and display any graphics. */  
            EDT_NULL,  
```

```
▁▁▁▁▁▁▁▁ | // | ! | ▁An | ▁en | um | ▁for | ▁all | ▁types | ▁of | ▁drivers | ▁the
▁Ir | r | l | ich | t | ▁Engine | ▁supports | . | ▁▁ | ↵▁ | ▁▁▁▁▁▁▁ | en
um | ▁E | _D | RI | VER | _T | Y | PE | ▁▁ | ↵▁ | ▁▁▁▁▁▁▁ | {
▁▁ | ↵▁▁▁▁▁▁▁▁▁▁▁▁ | // | ! | ▁N | ull | ▁driver | , | ▁useful | ▁for | ▁applications | ▁to
▁run | ▁the | ▁engine | ▁without | ▁visual | isation | . | ▁▁ | ↵▁▁▁▁▁▁▁▁▁▁▁▁ | /** | ▁The | ▁null
▁device | ▁is | ▁able | ▁to | ▁load | ▁textures | , | ▁but | ▁does | ▁not | ▁▁ | ↵▁▁▁▁▁▁▁▁▁▁▁▁
re | nder | ▁and | ▁display | ▁any | ▁graphics | . | ▁ | */ | ▁▁ | ↵▁▁▁▁▁▁▁▁▁▁▁▁ | ED
T | _N | U | LL | , | ▁▁ | ↵
```

### 6. Comment-heavy C++

Row 85 (0-based in this shard), lines 2–12. C++. `Nemotron-Pretraining-Code-v1`. `2833ca3c-67ae-49b3-9457-f36e2769e727`.

GDI+ file header. The line breaks in this block are CRLF. Excerpt: **99** tokens. Whole document: 804 tokens, 2359 bytes.

```
/*
 * gdiplusbase.h
 *
 * GDI+ base class with custom memory allocation
 *
 * This file is part of the w32api package.
 *
 * Contributors:
 *   Created by Markus Koenig <markus@stber-koenig.de>
 *
 * THIS SOFTWARE IS NOT COPYRIGHTED
```

```
/* | ␍ | ↵▁ | * | ▁g | di | plus | base | .h | ␍ | ↵▁ | *
␍ | ↵▁ | * | ▁G | DI | + | ▁base | ▁class | ▁with | ▁custom | ▁memory | ▁allocation
␍ | ↵▁ | * | ␍ | ↵▁ | * | ▁This | ▁file | ▁is | ▁part | ▁of | ▁the
▁w | 3 | 2 | ap | i | ▁package | . | ␍ | ↵▁ | * | ␍ | ↵▁
* | ▁Cont | rib | utors | : | ␍ | ↵▁ | * | ▁▁▁ | C | reated | ▁by
▁Mark | us | ▁K | oen | ig | ▁ | < | mark | us | @ | st | ber
-k | oen | ig | . | de | > | ␍ | ↵▁ | * | ␍ | ↵▁ | *
▁TH | IS | ▁SO | FT | W | ARE | ▁IS | ▁NOT | ▁CO | P | Y | RI
GH | TED | ␍↵
```

### 7. Comment-heavy Python

Row 155 (0-based in this shard), lines 2–13. Python. `Nemotron-Pretraining-Code-v2`. `c3db753c-5795-43b1-9239-bc35f0d02bdb`.

A linked-list solution whose type stub is entirely comments. Excerpt: **143** tokens. Whole document: 349 tokens, 1244 bytes.

```
# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def mergeInBetween(self, list1: ListNode, a: int, b: int, list2: ListNode) -> ListNode:
        # Find the (a-1)-th node to connect to list2
        prev = list1
        for _ in range(a - 1):
            prev = prev.next
```

```
# | ▁Definition | ▁for | ▁sing | ly | -l | ink | ed | ▁list | . | ↵ | #
▁class | ▁List | N | ode | : | ↵ | # | ▁▁▁▁ | ▁def | ▁ | __ | in
it | __ | ( | self | , | ▁val | = | 0 | , | ▁next | =None | ):
↵ | # | ▁▁▁▁▁▁▁▁ | ▁self | . | val | ▁ | = | ▁val | ↵ | # | ▁▁▁▁▁▁▁▁
▁self | . | next | ▁ | = | ▁next | ↵ | ↵ | class | ▁Solution | : | ↵▁
▁▁▁ | def | ▁merge | In | B | etween | ( | self | , | ▁list | 1 | :
▁List | N | ode | , | ▁a | : | ▁int | , | ▁b | : | ▁int | ,
▁list | 2 | : | ▁List | N | ode | ) | ▁ | -> | ▁List | N | ode
: | ↵▁ | ▁▁▁▁▁▁▁ | # | ▁Find | ▁the | ▁ | (a | - | 1 | )- | th
▁node | ▁to | ▁connect | ▁to | ▁list | 2 | ↵▁ | ▁▁▁▁▁▁ | ▁prev | ▁ | = | ▁list
1 | ↵▁ | ▁▁▁▁▁▁ | ▁for | ▁ | _ | ▁in | ▁range | (a | ▁ | - | ▁
1 | ): | ↵▁▁▁▁▁▁▁▁▁ | ▁▁ | ▁prev | ▁ | = | ▁prev | . | next | ↵
```

### 8. Strings

Row 0 (0-based in this shard), lines 8–20. Python. `Nemotron-Pretraining-Code-v1`. `e2c721a2-b05b-489a-9992-16b9fafbba74`.

A unicode spec template stored in one triple-quoted string. Excerpt: **155** tokens. Whole document: 939 tokens, 2660 bytes.

```
spec_file_content = u"""Name: boss
Version: 0.6.1
Release:1%{?dist}
Summary: MeeGo Build Orchestration Server System
Group: Productivity/Networking/Web/Utilities
License: GPL2
URL: http://wiki.meego.com/BOSS
Source0: boss_%{version}.orig.tar.gz
BuildRoot: %{name}-root-%(%{__id_u} -n)

%description
This description has some unicode: \xe1\xe1\xe1
"""
```

```
s | pec | _file | _cont | ent | ▁ | = | ▁u | "" | " | Name | :
▁boss | ↵ | V | ers | ion | : | ▁ | 0 | . | 6 | . | 1
↵ | Re | lease | : | 1 | % | { | ? | dist | } | ↵ | Summary
: | ▁Me | e | Go | ▁Build | ▁Or | che | str | ation | ▁Ser | ver | ▁System
↵ | Group | : | ▁Product | ivity | /N | et | working | / | We | b | /
U | t | ilities | ↵ | L | ic | ense | : | ▁GP | L | 2 | ↵
UR | L | : | ▁h | ttp | :// | w | iki | . | me | ego | .com
/B | OS | S | ↵ | Source | 0 | : | ▁boss | _ | % | { | version
}. | or | ig | .t | ar | .g | z | ↵ | Build | R | oot | :
▁ | % | { | name | } | - | root | - | % | ( | % | {
__ | id | _u | } | ▁ | -n | ) | ↵ | ↵ | % | des | cription
↵ | This | ▁description | ▁has | ▁some | ▁un | ic | ode | : | ▁ | \x | e
1 | \x | e | 1 | \x | e | 1 | ↵ | "" | " | ↵
```

### 9. Strings

Row 122 (0-based in this shard), lines 16–25. Python. `Nemotron-Pretraining-Code-v1`. `68800056-dec7-4663-bd9c-4f8b31ec1e1c`.

A style dictionary. The values are string literals. Excerpt: **92** tokens. Whole document: 1628 tokens, 5572 bytes.

```
# Page layout
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}
```

```
# | ▁Page | ▁layout | ↵ | SI | DE | B | AR | _ | ST | Y | LE
▁ | = | ▁ | { | ↵▁ | ▁▁▁ | " | position | ": | ▁ | "f | ixed
", | ↵▁ | ▁▁▁ | " | top | ": | ▁ | 0 | , | ↵▁ | ▁▁▁ | "
left | ": | ▁ | 0 | , | ↵▁ | ▁▁▁ | "b | ottom | ": | ▁ | 0
, | ↵▁ | ▁▁▁ | " | width | ": | ▁ | " | 1 | 6 | rem | ",
↵▁ | ▁▁▁ | "p | adding | ": | ▁ | " | 2 | rem | ▁ | 1 | rem
", | ↵▁ | ▁▁▁ | "b | ackground | -col | or | ": | ▁ | " | # | f
8 | f | 9 | fa | ", | ↵ | } | ↵
```

### 10. Strings

Row 108 (0-based in this shard), lines 8–10. Python. `Nemotron-Pretraining-Code-v2`. `90d1fb83-09e6-49af-821b-267bcd80eb3c`.

Quoted label inventories on three comment lines. Excerpt: **137** tokens. Whole document: 2287 tokens, 6322 bytes.

```
# TASK1: 'NO', 'YES'
# TASK2: '-', 'JUDGEMENTAL', 'REPORTED', 'DIRECT', 'UNKNOWN'
# TASK3:  'OBJECTIFICATION', 'STEREOTYPING-DOMINANCE', '-', 'MISOGYNY-NON-SEXUAL-VIOLENCE', 'IDEOLOGICAL-INEQUALITY', 'SEXUAL-VIOLENCE', 'UNKNOWN'
```

```
# | ▁T | AS | K | 1 | : | ▁' | NO | ', | ▁' | Y | ES
' | ↵ | # | ▁T | AS | K | 2 | : | ▁ | '- | ', | ▁'
J | UD | G | EM | ENT | AL | ', | ▁' | RE | P | OR | TED
', | ▁' | DI | RE | CT | ', | ▁' | UN | K | N | OW | N
' | ↵ | # | ▁T | AS | K | 3 | : | ▁ | ▁' | O | B
J | EC | TI | F | ICA | TION | ', | ▁' | S | TE | RE | OT
Y | P | ING | - | DO | M | IN | A | NCE | ', | ▁ | '-
', | ▁' | M | IS | OG | Y | N | Y | -N | ON | - | SE
X | U | AL | -V | I | O | LE | NCE | ', | ▁' | I | DE
OL | OG | ICA | L | - | INE | QU | AL | ITY | ', | ▁' | SE
X | U | AL | -V | I | O | LE | NCE | ', | ▁' | UN | K
N | OW | N | ' | ↵
```

### 11. Math

Row 200 (0-based in this shard), lines 4–9. Python. `Nemotron-Pretraining-Code-v2`. `cb691ed6-409d-4d83-8077-b55b96746cfe`.

NumPy matrix shapes: `zeros`, `ones`, and `eye`. Excerpt: **114** tokens. Whole document: 574 tokens, 1610 bytes.

```
if __name__ == '__main__':
    zeros_array = np.zeros((3, 4))  # Create a 3x4 matrix of zeros
    ones_array = np.ones((3, 4))    # Create a 3x4 matrix of ones
    
    identity_3x3 = np.eye(3)        # 3x3 identity matrix
    identity_3x4 = np.eye(3, 4)     # 3x4 identity-like matrix
```

```
if | ▁ | __ | name | __ | ▁ | == | ▁ | ' | __ | main | __
': | ↵▁ | ▁▁▁ | zeros | _array | ▁ | = | ▁np | .zeros | (( | 3 | ,
▁ | 4 | )) | ▁▁ | # | ▁Create | ▁a | ▁ | 3 | x | 4 | ▁matrix
▁of | ▁zeros | ↵▁ | ▁▁▁ | ones | _array | ▁ | = | ▁np | .ones | (( | 3
, | ▁ | 4 | )) | ▁▁▁▁ | # | ▁Create | ▁a | ▁ | 3 | x | 4
▁matrix | ▁of | ▁ones | ↵▁ | ▁▁▁ | ↵▁ | ▁▁▁ | identity | _ | 3 | x | 3
▁ | = | ▁np | .eye | ( | 3 | ) | ▁▁▁▁▁▁▁▁ | # | ▁ | 3 | x
3 | ▁identity | ▁matrix | ↵▁ | ▁▁▁ | identity | _ | 3 | x | 4 | ▁ | =
▁np | .eye | ( | 3 | , | ▁ | 4 | ) | ▁▁▁▁▁ | # | ▁ | 3
x | 4 | ▁identity | -like | ▁matrix | ↵
```

### 12. Byte fallback

Row 4 (0-based in this shard), line 3. C++. `Nemotron-Pretraining-Code-v1`. `91aa5151-1953-4a2e-9e13-93add755e110`.

One C++ comment in Chinese. Each UTF-8 byte of the Han characters is its own piece. Excerpt: **44** tokens. Whole document: 1815 tokens, 4437 bytes.

```
// 基于线性探测的符号表(哈希表)
```

```
// | ▁ | <0xE5> | <0x9F> | <0xBA> | <0xE4> | <0xBA> | <0x8E> | <0xE7> | <0xBA> | <0xBF> | <0xE6>
<0x80> | <0xA7> | <0xE6> | <0x8E> | <0xA2> | <0xE6> | <0xB5> | <0x8B> | <0xE7> | <0x9A> | <0x84> | <0xE7>
<0xAC> | <0xA6> | <0xE5> | <0x8F> | <0xB7> | <0xE8> | <0xA1> | <0xA8> | ( | <0xE5> | <0x93> | <0x88>
<0xE5> | <0xB8> | <0x8C> | <0xE8> | <0xA1> | <0xA8> | ) | ↵
```

