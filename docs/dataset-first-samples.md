---
cursor:
  subagentId: "bc-a5cdca27-cecc-519d-9c0c-5bb3ed69803b"
---

# First document from each training dataset

One document from each dataset the tokenization plan will train on. Bucket `s3://nemotron-training-data-us-east-1/`, region `us-east-1`. Each sample is the first row of the first data object in S3 key order. Parquet was read with byte ranges: the footer, then the first page of the text column (and the dictionary page when that column is dictionary-encoded). The object was not downloaded. IndicCorp is plain text, one document per line; only the start of the file was read.

Skipped: `translation-staging/`, `gzip6/` score files, `*_Latn`, Sangraha `verified/eng`, and every language outside Hindi, Bengali, Tamil, Telugu, Kannada, Marathi, and Gujarati. Genesis failure-analysis rows were not taken. English HQ synth is the Nemotron-CC v2.1 text at `translations/Cosmopedia-v2/Krutrim/source-snapshots/Nemotron-CC-v2.1/High-Quality-Synthetic/`, not the TinyLlama pack.

Character length is the number of Unicode code points in the full document. A document longer than 1,500 characters is cut to the first 700 and the last 700. The text is otherwise unchanged.

Cosmopedia v5, among these seven languages, has folders only for Kannada and Marathi. Hindi, Bengali, Tamil, Telugu, and Gujarati are not in v5, so those samples are the first document of the v4 run.

Fact-Seeking Indic was checked on each object opened. The column named `translation` is the translated text. `translation_sha256` is a 64-character hex digest. The sample is `translation`.

## What is here

### English index

- ClimbMix: 1,051 characters
- Math 4+: 2,330 characters
- MIND: 3,189 characters
- RQA: 11,370 characters
- Fact-Seeking: 145 characters
- Specialized v1.1: 3,081 characters
- CodeAlchemy: 27,675 characters
- Nemotron Code v2: 2,660 characters
- HQ synth: 1,509 characters
- Genesis III: 4,344 characters
- InfiniByte: 51,883 characters

### Indic index

- Sangraha verified — Hindi: 2,478 characters
- Sangraha verified — Bengali: 1,438 characters
- Sangraha verified — Tamil: 1,489 characters
- Sangraha verified — Telugu: 1,690 characters
- Sangraha verified — Kannada: 832 characters
- Sangraha verified — Marathi: 2,522 characters
- Sangraha verified — Gujarati: 2,202 characters
- Sangraha synthetic — Hindi: 907 characters
- Sangraha synthetic — Bengali: 449 characters
- Sangraha synthetic — Tamil: 3,020 characters
- Sangraha synthetic — Telugu: 366 characters
- Sangraha synthetic — Kannada: 2,237 characters
- Sangraha synthetic — Marathi: 1,031 characters
- Sangraha synthetic — Gujarati: 4,278 characters
- Sangraha unverified — Hindi: 1,355 characters
- Sangraha unverified — Bengali: 4,489 characters
- Sangraha unverified — Tamil: 1,584 characters
- Sangraha unverified — Telugu: 671 characters
- Sangraha unverified — Kannada: 2,821 characters
- Sangraha unverified — Marathi: 1,157 characters
- Sangraha unverified — Gujarati: 3,552 characters
- FineWeb 2 — Hindi: 1,945 characters
- FineWeb 2 — Bengali: 18,827 characters
- FineWeb 2 — Tamil: 907 characters
- FineWeb 2 — Telugu: 596 characters
- FineWeb 2 — Kannada: 5,274 characters
- FineWeb 2 — Marathi: 785 characters
- FineWeb 2 — Gujarati: 2,177 characters
- IndicCorp v2 — Hindi: 45 characters
- IndicCorp v2 — Bengali: 410 characters
- IndicCorp v2 — Tamil: 314 characters
- IndicCorp v2 — Telugu: 201 characters
- IndicCorp v2 — Kannada: 16 characters
- IndicCorp v2 — Marathi: 527 characters
- IndicCorp v2 — Gujarati: 54 characters
- BhashaWiki — Hindi: 2,082 characters
- BhashaWiki — Bengali: 2,057 characters
- BhashaWiki — Tamil: 2,334 characters
- BhashaWiki — Telugu: absent
- BhashaWiki — Kannada: 2,153 characters
- BhashaWiki — Marathi: absent
- BhashaWiki — Gujarati: 2,031 characters
- Cosmopedia — Hindi: 3,468 characters
- Cosmopedia — Bengali: 4,145 characters
- Cosmopedia — Tamil: 2,986 characters
- Cosmopedia — Telugu: 5,473 characters
- Cosmopedia — Kannada: 3,327 characters
- Cosmopedia — Marathi: 3,288 characters
- Cosmopedia — Gujarati: 2,232 characters
- Indic HQ-synthetic — Hindi: 1,750 characters
- Indic HQ-synthetic — Bengali: 2,026 characters
- Indic HQ-synthetic — Tamil: 3,984 characters
- Indic HQ-synthetic — Telugu: 5,952 characters
- Indic HQ-synthetic — Kannada: absent
- Indic HQ-synthetic — Marathi: 1,719 characters
- Indic HQ-synthetic — Gujarati: 10,409 characters
- Fact-Seeking Indic — Hindi: 192 characters
- Fact-Seeking Indic — Bengali: 312 characters
- Fact-Seeking Indic — Tamil: 551 characters
- Fact-Seeking Indic — Telugu: 335 characters
- Fact-Seeking Indic — Kannada: 479 characters
- Fact-Seeking Indic — Marathi: 118 characters
- Fact-Seeking Indic — Gujarati: 216 characters

## English

### ClimbMix

- **S3 key:** `datasets/nemotron-climbmix/karpathy-400b-shuffle/shard_00000.parquet`
- **Column:** `text`
- **Document id:** none. This file has no id column.
- **Character length:** 1,051

```
Protect your business and employee's during flu seaon

Starting in 2005, the Center for Disease Control (CDC) established the National Influenza Vaccination week "to highlight the importance of continuing flu vaccination through the holiday season and beyond." In 2017, by the end of November only about 41% of the recommended US population had been vaccinated.

If you've already gotten the flu, you can still get vaccinated to protect you against other strands of the flu, according to the CDC. People with high risk of complications from the flu include young children, pregnant women, people with certain chronic health conditions and people over the age of 65, and should get vaccinated. Although anyone is at risk of getting the flu, for high-risk people, hospitalization or death is more likely than for others.

According to the CDC, "flu vaccination can reduce flu illnesses, doctors' visits and missed work and school due to flu, as well as prevent flu-related hospitalizations." Get a flu shot today to protect yourself and your loved ones.
```


### Math 4+

- **S3 key:** `datasets/nemotron-cc-math-v1/4plus/part_000000.parquet`
- **Column:** `text`
- **Document id:** `fb5913e0-9097-41ef-be69-728a148079f5` (column `id`)
- **Character length:** 2,330

The first 700 characters, then the last 700. 930 characters were cut from the middle.

```
# Jane Street

This employer has taken extra steps to respond to reviews and provide job seekers with accurate company information, photos, and reviews. Interested for your company? Learn More.

- Overview
- Reviews
- Salaries
- Interviews
- Jobs
- Photos
- Benefits

18 Reviews | 54 Salaries | 465 Interviews

## Interview Question

### Trader Intern Interview, New York, NY

**Jane Street**

What is the smallest number divisible by 225 that consists of all 1s and 0s?

**Tags:**

## Answer

6 Answers

### Interview Answer

Two facts to note are:
1. Multiples of 225 end in 00, 25, 50, 75.
2. A number is divisible by 9 if the digits sum to 9.

Only those multiples ending in 00 could have only 1'
```


930 characters cut

```
*Anonymous is wrong on 14/07/2012**

3. I fail to understand the above answers. Shouldn't it be 225 or 2250. \( 225 \div 225 = 1 \) and \( 2250 \div 225 = 10 \). Both these numbers contain just 1's and 0's.  
   **Anonymous on 11/10/2013**

4. The above answers seem too complicated/not explained at all.  
   First, notice that \( 225 = 25 \times 9 \).  
   (1) A number is divisible by 9 if and only if the sum of its digits is divisible by 9. We must have 9 1's in our number.  
   (2) A number is divisible by 25 if and only if the last two digits are divisible by 25. Our last two digits must be 0's.  
   Putting (1) and (2) together, our number is 11111111100.  
   **Anonymous on 09/09/2014**
```


### MIND

- **S3 key:** `datasets/nemotron-cc-math-v1/4plus_MIND/part_000000.parquet`
- **Column:** `text`
- **Document id:** `85fcda50-f571-4ccc-b910-b2a258f8bc26` (column `id`)
- **Character length:** 3,189

The first 700 characters, then the last 700. 1,789 characters were cut from the middle.

```
**Debate on NonEuclidean Geometry Concepts**

**Participant A:** Let's focus on the Hyperbolic Geometry example first. The model describes a scenario where given a line \( l \) and a point \( P \), the lines \( PX \) and \( PY \) are parallels through \( P \) to \( l \). This is because they intersect the boundary circle at points \( X \) and \( Y \). 

**Participant B:** I agree with your summary. However, it's important to note that in other models, the concept of parallels is not as straightforward. For instance, sometimes there are unique parallels and sometimes many. The context describes a line \( l \) where the entire Euclidean line is in \( S \), and a point \( P \) in the halfplane 
```


1,789 characters cut

```
a unique line through the origin.

**Participant B:** Yes, any great circle through \( P \) also passes through \(-P\). If \(\{P, -P\}\) is distinct from \(\{Q, -Q\}\), then \( P \) and \( Q \) are not antipodal, and there is a unique great circle through them, intersecting at \(-P\) and \(-Q\).

**Participant A:** And any two great circles intersect at two points, \( P \) and \(-P\), which are considered a single point in the Riemann projective plane, ensuring the unique intersection of the two lines.

**Participant B:** This comprehensive understanding of the models and transformations highlights the intricate nature of non-Euclidean geometry and its consistent adherence to defined axioms.
```


### RQA

- **S3 key:** `datasets/Nemotron-Pretraining-Specialized-v1/Nemotron-Pretraining-RQA/part_000000.parquet`
- **Column:** `text`
- **Document id:** `4674f31f-6a94-40e0-bcc5-0f8c358b703f` (column `uuid`)
- **Character length:** 11,370

The first 700 characters, then the last 700. 9,970 characters were cut from the middle.

```
Question: Consider an asymmetric encryption scheme Π proven IND-CCA2 secure in the random oracle model under the assumption that a trapdoor permutation family F is *partial-domain one-way* (PDOW). Suppose a subsequent analysis demonstrates that for the specific instantiation using permutation f, PDOW(f) is computationally equivalent to the standard one-wayness (OW) of f. However, the IND-CCA2 security reduction for Π exhibits a non-tight loss factor of O(2^λ) in the adversary's advantage, where λ is the security parameter. Meanwhile, an alternative scheme Π' achieves IND-CCA2 security under the standard OW assumption with a tight reduction (loss factor O(1)), but requires additional algebrai
```


9,970 characters cut

```
ng its use of algebraic structure.  

> **Final verdict**: The claim is incorrect. **Reduction tightness and implementation security dominate assumption strength** in practice. For real-world deployment, Π' is superior despite its structural requirements. Always prioritize *concrete security* over asymptotic assumption hierarchies when reductions are non-tight.  

--- 
**References for framework**:  
- Tightness: [Katz & Wang, EUROCRYPT 2003] on concrete security.  
- Side channels: [Bellare et al., CRYPTO 2009] on RO model limitations; [Dziembowski & Pietrzak, FOCS 2008] on leakage resilience.  
- Assumption equivalence: [Fujisaki et al., J. Cryptology 2001] clarifies PDOW/OW relationships.
```


### Fact-Seeking

- **S3 key:** `datasets/Nemotron-Pretraining-Specialized-v1.2/Nemotron-Pretraining-Fact-Seeking/part_000000.parquet`
- **Column:** `text`
- **Document id:** `76a8239d-d0d8-4a52-a315-a43b49069f63` (column `uuid`)
- **Character length:** 145

```
How many times was the 10th Tank Corps formed during its history in the Red Army?
A. Once
B. Three times
C. Twice
D. Four times
Answer: C. Twice
```


### Specialized v1.1

- **S3 key:** `datasets/Nemotron-Pretraining-Specialized-v1.1/Nemotron-Pretraining-Code-Concepts/part_000000.parquet`
- **Column:** `text`
- **Document id:** `daef56fd-7b41-4c73-b585-ec135b880262` (column `uuid`)
- **Character length:** 3,081

The first 700 characters, then the last 700. 1,681 characters were cut from the middle.

```
from typing import List, Tuple

def detect_no_dup_range_gcd_mod(nums: List[int], queries: List[Tuple[int, int]], mod: int) -> List[int]:
    """Return the GCD modulo `mod` for each subarray [l, r] in `queries` if the subarray contains no duplicate values; otherwise return 0 for that query.

    The function expects 0‑based indices in `queries`.  
    It processes each query independently.

    Examples:
    >>> detect_no_dup_range_gcd_mod([2,4,3,6,5], [(0,4), (1,3), (2,2)], 1000)
    [1, 1, 3]
    >>> detect_no_dup_range_gcd_mod([1,2,1,4], [(0,3), (1,2)], 7)
    [0, 1]
    >>> detect_no_dup_range_gcd_mod([9,15,7], [(0,2)], 5)
    [1]
    """
    # ---------- helper ----------
    def _gcd(a:
```


1,681 characters cut

```
      return a if a < b else b

    def range_gcd(l: int, r: int) -> int:
        """gcd of nums[l..r] (inclusive)."""
        length = r - l + 1
        k = length.bit_length() - 1
        a = st_gcd[k][l]
        b = st_gcd[k][r - (1 << k) + 1]
        return _gcd(a, b)

    # ---------- 4. answer each query ----------
    ans = []
    for l, r in queries:
        if l > r:                         # just in case, enforce order
            l, r = r, l
        # duplicate?  if the smallest next occurrence inside [l,r] lies inside the interval
        if range_min(l, r) <= r:
            ans.append(0)
        else:
            g = range_gcd(l, r)
            ans.append(g % mod)
    return ans
```


### CodeAlchemy

- **S3 key:** `datasets/codealchemy/code-dev/train-00013-of-00252.parquet`
- **Column:** `text_with_placeholders`
- **Document id:** `eaf106fb31f9494e74123b87bb958cd573a15b83` (column `blob_id`)
- **Character length:** 27,675
- **Note:** this file has no `text` column. The text is `text_with_placeholders`.

The first 700 characters, then the last 700. 26,275 characters were cut from the middle.

```
User:
Take the `QML::AppRunner` from prompt 2 and evolve it further by introducing asynchronous execution using Ruby's `EventMachine`. The new class `QML::AsyncRunner` must:

1. Accept an optional `:timeout` parameter (seconds). If the event loop exceeds this timeout, it should abort the native loop and raise `TimeoutError`.
2. Run the native event loop in a separate thread to avoid blocking the main Ruby thread.
3. Use `rb_thread_call_without_gvl` with the `RUBY_UBF_IO` flag to ensure the GIL is released during the native call.
4. Provide a callback mechanism (`on_exit`) that Ruby code can register to receive the exit code once the loop finishes or times out.
5. Handle race conditions where
```


26,275 characters cut

```
_quit` with the real API that stops the native loop.  
* If your native library provides a more efficient way to abort (e.g. a `quit()` method that is safe to call from any thread), use that instead of the placeholder.  
* Because the native loop runs in its own thread, you must be careful not to access Ruby objects from that thread unless you have a GVL.  All Ruby calls are marshalled back onto the main thread via the Ruby API (e.g. `rb_funcall` inside the thread).  

With these pieces in place you now have a fully‑featured, thread‑safe, timeout‑aware asynchronous runner that integrates cleanly with Ruby’s EventMachine ecosystem while preserving the familiar synchronous API for legacy code.
```


### Nemotron Code v2

- **S3 key:** `datasets/nemotron-code-v2/synthetic-code-review/part_00005.parquet`
- **Column:** `content`
- **Document id:** `e2c721a2-b05b-489a-9992-16b9fafbba74` (column `nemotron_pretraining_id`)
- **Character length:** 2,660
- **Note:** Nemotron Code v2 stores the document in `content`.

The first 700 characters, then the last 700. 1,260 characters were cut from the middle.

````
```py
import unittest
from unittest.mock import Mock

from common_test_lib import BaseTestParticipantHandler, WI_TEMPLATE
from RuoteAMQP.workitem import Workitem

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

class TestParticipantHandler(BaseTestParticipantHandler):

    module_under_test = "check_spec"

    def setUp(self):
        super().setUp()
        self.fake_actions = ["build", "test
````


1,260 characters cut

````
log"

        self.participant.handle_wi(wid)
        self.assertFalse(wid.result)

    def test_bad_workitem(self):
        wid = Workitem(WI_TEMPLATE)
        with self.assertRaises(ValueError):
            self.participant.handle_wi(wid)


if __name__ == '__main__':
    unittest.main()
```

Code review identified several areas for improvement:
1. Added assertions to 'test_handle_wi_control' and 'test_setup_obs'.
2. Fixed syntax error in 'test_handle_lifecycle_control' by using 'Mock()'.
3. Defined 'self.fake_actions' via a helper setup.
4. Refactored Workitem setup into a helper method.
5. Updated mock imports for Python 3 compatibility.
6. Corrected exception type in 'test_bad_workitem'.
````


### HQ synth

- **S3 key:** `translations/Cosmopedia-v2/Krutrim/source-snapshots/Nemotron-CC-v2.1/High-Quality-Synthetic/part_000000.parquet`
- **Column:** `text`
- **Document id:** `0f817001-346d-4ae0-bf9f-370fae3eed57` (column `uuid`)
- **Character length:** 1,509

The first 700 characters, then the last 700. 109 characters were cut from the middle.

```
The Knitting Pilgrim is a one-man show by Kirk Dunn, an actor and knitter from Toronto, which is touring in British Columbia for the first time in April with performances in several cities. Dunn began creating three large knitted tapestries in 2003, each representing the Abrahamic religions of Judaism, Christianity, and Islam, and completed them in 2018. Unable to find a gallery to exhibit them, he created a theatre show to share his work. The show, co-written by his wife Claire Ross Dunn, debuted in 2019 and features storytelling, image projection, and knitted panels resembling stained-glass windows. Audience members are encouraged to knit while Dunn discusses his artistic journey as an ord
```


109 characters cut

```
ween acting jobs, and after being encouraged by a museum director, he began creating installations. Inspired by his background as a preacher's kid and the events after 9/11, he explored the tensions between the three major faiths. The project took much longer than expected, leading to self-doubt, financial challenges, and strain on his marriage. The tapestries are stored in rolled-up form in chest freezers to protect them from light and pests. During performances, they are unrolled and displayed behind projection screens. Dunn emphasizes the ongoing relevance of the tapestries' themes, noting that the show is not preachy but rather raises questions about how people can move forward together.
```


### Genesis III

- **S3 key:** `datasets/genesis-iii/astronomy/train-00002-of-00018.parquet`
- **Column:** `text`
- **Document id:** none. This file has no id column.
- **Character length:** 4,344
- **Pipeline:** `option_level`

The first 700 characters, then the last 700. 2,944 characters were cut from the middle.

```
**User:** Hey, I’ve got this question here about galaxies, and I’m a little stuck. It says: *“Which type of galaxy has a central bar structure?”* The options are A. Spiral, B. Elliptical, C. Barred spiral, D. Irregular. Hmm, I think I remember something about barred spirals, but I want to make sure I’m not mixing things up. Can you help me break this down?  

**Assistant:** Of course! Let’s start by unpacking the question. Why do you think understanding galaxy types matters?  

**User:** Well, I guess it’s about classifying galaxies based on their shapes, right? Like, how they look through telescopes? But I’m still fuzzy on the specifics.  

**Assistant:** Exactly! The Hubble sequence classi
```


2,944 characters cut

```
classification questions in the future?  

**Assistant:** First, **remember the Hubble sequence**: elliptical → spiral (including barred spiral) → irregular. Second, **look for keywords** in the question. Here, "central bar" immediately points to barred spirals. Third, **eliminate obviously wrong options** first (like elliptical or irregular). Lastly, **visualize the features**—drawing a quick sketch can help!  

**User:** Perfect! So the answer is definitely C. Barred spiral.  

**Assistant:** Yep! \boxed{C}  

**User:** Thanks so much! This really helped me see how to break down the question step by step.  

**Assistant:** Anytime! You’re doing great—keep asking those clarifying questions!
```


### InfiniByte

- **S3 key:** `datasets/Nemotron-Pretraining-Specialized-v1/Nemotron-Pretraining-InfiniByte-Reasoning/part_000000.parquet`
- **Column:** `text`
- **Document id:** `fa3e4839-368c-449a-9245-641a6187a4c5` (column `uuid`)
- **Character length:** 51,883

The first 700 characters, then the last 700. 50,483 characters were cut from the middle.

```
Question: Alice is climbing stairs in a laboratory where the air is filled with tiny droplets of a special liquid. Each day, she climbs A stairs upwards, but at night, she slides down B stairs due to the liquid's resistance. The boiling point of the liquid decreases with decreasing droplet size due to surface tension effects. Given the initial boiling point ( T_b ), the enthalpy of vaporization ( ΔH_vap ), the surface tension ( σ ), the molar volume ( V ), the gas constant ( R ), and the temperature ( T ), calculate the number of days Alice will take to reach the top of the staircase, considering that the effective resistance changes as the boiling point of the liquid decreases, affecting th
```


50,483 characters cut

```

3. **Immediate Check**: If `A` is sufficient to reach `N` in one day, output `1`. If `effective_B` is greater than or equal to `A`, output `-1` as progress is impossible.
4. **Cycle Calculation**: For other cases, compute the number of full cycles (`d_cycle`) needed to cover `N - A` stairs, where each cycle nets `A - effective_B` stairs. The ceiling of this division ensures we account for partial cycles. The total days is `d_cycle + 1` (the final day without sliding).
5. **Output**: The result is printed as an integer.

This approach efficiently models the problem by adjusting the nightly slide based on temperature and applying classic staircase climbing logic with variable nightly descent.
```


## Indic

### Sangraha verified — Hindi

- **S3 key:** `datasets/sangraha/verified/hin/data-0.parquet`
- **Column:** `text`
- **Document id:** `c729b49b2d13dea710df863877cb3266df6e1a9e` (column `doc_id`)
- **Character length:** 2,478

The first 700 characters, then the last 700. 1,078 characters were cut from the middle.

```
अमेरिकी राष्ट्रपति चुनाव (US Presidential Election) के दिन नासा (NASA) की एस्ट्रॉनॉट केट रूबिन्स (Kate Rubins) अंतरिक्ष से वोट देंगी. 1997 में नासा के डेविड वूल्फ पहले एस्ट्रॉनॉट थे, जिन्होंने स्पेस से वोटिंग की थी. प्रश्न यह है कि स्पेस से वोटिंग होती कैसे है?
 इंटरनेशनल स्पेस स्टेशन (ISS) धरती से 200 मील दूर स्थित है और पृथ्वी की कक्षा में 17000 मील प्रति घंटे से चक्कर लगाता है. अब मुद्दा ये है कि जिस दिन अमेरिका में चुनाव होंगे, उस दिन कुछ अंतरिक्ष यात्री यानी एस्ट्रॉनॉट्स अंतरिक्ष में होंगे, तो वो वोट कैसे देंगे? खबरों में कहा गया है कि आईएसएस का मिशन चूंकि छह महीने से पहले खत्म होना मुश्किल है इसलिए एस्ट्रॉनॉट अंतरिक्ष से ही अपना वोट देंगे. कैसे? इसके लिए एक खास व्यवस्था हुई है.
 एस्ट्र
```


1,078 characters cut

```
 को एक एन्क्रिप्टेड ई मतपत्र अपलिंक हो जाता है. ईमेल से एस्ट्रॉनॉट को जो यूनिक प्रमाण पत्र भेजे गए होते हैं, उनका इस्तेमाल करते हुए एस्ट्रॉनॉट अपना वोट देते हैं और भेजे गए अपलिंक को पृथ्वी पर उतरने के बाद वो डाउनलिंक कर इसकी सूचना काउंटी के क्लर्क दफ्तर में देते हैं.
 इंटरनेशनल स्पेस स्टेशन (ISS) धरती से 200 मील दूर स्थित है और पृथ्वी की कक्षा में 17000 मील प्रति घंटे से चक्कर लगाता है. अब मुद्दा ये है कि जिस दिन अमेरिका में चुनाव होंगे, उस दिन कुछ अंतरिक्ष यात्री यानी एस्ट्रॉनॉट्स अंतरिक्ष में होंगे, तो वो वोट कैसे देंगे? खबरों में कहा गया है कि आईएसएस का मिशन चूंकि छह महीने से पहले खत्म होना मुश्किल है इसलिए एस्ट्रॉनॉट अंतरिक्ष से ही अपना वोट देंगे. कैसे? इसके लिए एक खास व्यवस्था हुई है.
 
```


### Sangraha verified — Bengali

- **S3 key:** `datasets/sangraha/verified/ben/data-0.parquet`
- **Column:** `text`
- **Document id:** `7c2fe5a1ffd753aba26f090146edebcb` (column `doc_id`)
- **Character length:** 1,438

```
কি বলব? যা বলতে আসছি তা দেখছি সবাই আপনাকে বলেই দিয়েছে।একি স্টাইলের ধন্যবাদ আরেকবার দিতে চাচ্ছিনা।তবে আপনার এই প্রচেষ্টা আমাদের যততুকু সাহায্য করেছে তা ধন্যবাদের মত ছোট শব্দ দিয়ে প্রকাশ করা যায়না।মনে প্রানে আপনার জন্য দোয়া করছি।
আপনি যে কোন আরএসএস রিডার বা নিউজ রিডারে গিয়ে quranerkotha.com/feed যোগ করে দিন। এরপর থেকে নতুন আর্টিকেল বের হলে নিউজ রিডার আপনাকে জানিয়ে দেবে।
আলহামদুলিল্লাহ! অনেকদিন ধরে পড়ছি কমেনট করবো বলেও ভাবছিলাম। আর্টিকেলগুলো আমার খুবই ভালো লাগছে। সকলের জন্য অনেক দুয়া করছি। আল্লাহ আমাদের সকলকে কুরআন বুঝে তা অনুসরণ করার তৌফিক দান করুন। আমীন।
সত্যিই ভাই অসাধারণ এই সাইট টি। আল্লাহ আপনাদের হায়াত ও শান্তি দান করুক। ওমর আল জাবির ভাই আপ্নার ফেসবুক আইডি টা দিবেন প্লিজ,,,,,,!
অসাধারণ।ধন্যবাদ দিয়ে আপনাকে ছোট করব না।আপনার আর্টিকেলগুলো কি আমার ব্যক্তিগত ফেসবুক প্রোফাইলে কপি পেস্ট করতে পারি? সেখানে লিংক সহ উল্লেখ থাকবে।
আসসালামু আলাইকুম। প্রথমে আপনার জন্য আল্লাহর কাছে দোয়া করি। জাবির ভাই আমার বেশী আগ্রহ বিজ্ঞানের সাথে সম্পৃক্ত কুরআনের যে আয়াত গুলো রয়েছে তার উপর। আমি কিভাবে ভালো করে এইসব আয়াতের তাফসীর জানার ব্যাপারে আপনার থেকে সহযোগিতা পাবো। প্লিজ বললে আমার অনেক কাজে আসবে।
কতৃপক্ষের দৃষ্টি আকর্ষন করে বিলছি আপনাদের রেফারেন্স এ কিছু ভুল রয়েছে, ঋগ্বেদ এর ৭ঃ৪ঃ১১ ও ১ঃ১৬ঃ৪ এ যে দুটি স্লোক লিখা হয়েছে তা রেফারেন্স বই এ নেই, আপনাদের লিখা উক্তি দুটি হচ্ছে, [ঋগ্বেদ ১ : ১৬ঃ ৪ ] যারা তোমাকে পূজার উপহার দেয় না , তাদের প্রত্যেককে হত্যা করো ; যাদেরকে বোঝানো কঠিন , যারা তোমাকে তৃপ্ত করে না। ওদের সম্পদ আমাদেরকে দাও।
```


### Sangraha verified — Tamil

- **S3 key:** `datasets/sangraha/verified/tam/data-0.parquet`
- **Column:** `text`
- **Document id:** `d8467560df293124156db767026a1e930b96341d` (column `doc_id`)
- **Character length:** 1,489

```
புதுச்சேரி-நேருக்கு நேர் விவாதம் செய்தால் மீசை அல்ல, மொட்டையே அடித்துக் கொள்ள நேரிடும் என முன்னாள் அமைச்சருக்கு, கல்யாணசுந்தரம் எம். எல். ஏ. , சவால் விடுத்துள்ளார்.
 அவரது அறிக்கைஃ
காலாப்பட்டில் கடந்த 9ம் தேதி நடந்த காங். , நிர்வாகிகள் ஆலோசனைக் கூட்டத்தில் பேசிய முன்னாள் அமைச்சர் ஷாஜகான், அவர் கொண்டு வந்த திட்டங்களை நான் கொண்டு வந்ததாக கூறி மக்களை ஏமாற்றி வருவதாக தெரிவித்துள்ளார்.
 மேலும், என்னுடன் நேருக்கு நேர் விவாதிக்க போவதாகவும், அவ்வாறு இல்லை என நிருபித்தால், ஒருபக்க மீசையை எடுத்துக் கொள்வதாக சவால் விட்டுள்ளார்.
 அவரது சவால், எனது மக்கள் நலத்திட்ட பணிகளை மேலும் மேம்படுத்திக் கொள்ள வாய்ப்பாக கருதுகிறேன்.
 எந்த திட்டத்தை யார் கொண்டு வந்தது என்பது காலாப்பட்டு தொகுதி மக்களுக்கு நன்றாகவே தெரியும், நான், அவருடன் நேருக்கு நேர் விவாதம் செய்தால் அவ் மீசையை மட்டும் அல்ல மொட்டை அடித்துக் கொள்ள நேரிடும்.
 பிள்ளைச்சாவடி கடல் அரிப்பு சம்பந்தமாக அவர் பேசியதற்கு, நான் கடந்த டிசம்பர் 13ம் தேதி நேருக்கு நேர் பொது மேடையில் விவாதிக்க தயார் என அறைக்கூவல் விடுத்திருந்தேன். அதற்கு பதில் கூறாதவர் தற்போது தனியார் விடுதியில் நான்கு சுவற்றுக்கு மத்தியில் சவால் விடுத்திருப்பது சிறுபிள்ளைத்தனமாக உள்ளது.
 அவரது விருப்பத்தை போலவே, நேருக்கு நேர் பொது மேடையில் நான் கடந்த 2011 முதல் 2016 வரை ஆட்சியில் இருந்தபோதும், தற்போது 2021 முதல் இன்று வரை என்னென்ன திட்டங்கள் கொண்டு வந்து செயல்படுத்தியுள்ளேன் என ஆதாரத்துடன் விவாதம் செய்ய தயாராக உள்ளேன்.
 அதேபோன்று, அவர் கடந்த ஐந்தாண்டு கால ஆட்சியில் என்னென்ன திட்டங்கள் கொண்டு வந்தார் என்று ஆதாரத்துடன் பொதுமேடையில் அறிவிக்க தயாரா என கேள்வி எழுப்பி உள்ளார். 
```


### Sangraha verified — Telugu

- **S3 key:** `datasets/sangraha/verified/tel/data-0.parquet`
- **Column:** `text`
- **Document id:** `d2390203b0a4330a79c2af6973cbc7f5` (column `doc_id`)
- **Character length:** 1,690

The first 700 characters, then the last 700. 290 characters were cut from the middle.

```
భారత టెన్నిస్ స్టార్ సానియా మిర్జా దేని కోసం ఆరాటపడుతోందో తెలుసా..? అదే ఫ్రెంచ్ కిస్..గతంలో ఎన్నడూ లేని విధంగా ఈసారి మాత్రం ఈ హైదరాబాదీ బ్యూటీ ఫ్రెంచ్ ఓపెన్ పై ఎన్నో హోప్స్ పెట్టుకుంది. ఫ్రెంచ్ ఓపెన్ టైటిల్ ను గెలిస్తే..సానియా కెరియర్ స్లామ్ ను పూర్తి చేస్తుంది. ఇప్పటికే సానియా ఖాతాలో మూడు గ్రాండ్ స్లామ్ టైటిళ్లు ఉన్నాయి. డబుల్స్, మిక్స్ డ్ డబుల్స్ లో ఈ టైటిల్స్ సాధించింది. ఆస్ట్రేలియన్ ఓపెన్, యూఎస్ ఓపెన్, వింబుల్డన్ ట్రోఫీలను ముద్దాడిన సానియా, ఫ్రెంచ్ ఓపెన్ ట్రోఫీని కూడా ముద్దాడాలని ఆరాటపడుతోంది.
2015లాగే 2016 కూడా సానియాకు గోల్డెన్ ఇయర్ గా మారింది. 2015లో సానియా వింబుల్డన్, యూఎస్ ఓపెన్ టైటిల్స్ గెలవగా...2016లో ఆస్ట్రేలియన్ ఓపెన్ కిరీటం దక్కించుకుంది. ఇక ఈ ఏడాదిని నెంబర్ వన్ హోదాతోనే ముగించ
```


290 characters cut

```
టే ముందు ఆస్ట్రేలియన్ ఓపెన్ (జనవరి 2017లో)జరుగుతుంది. ఫ్రెంచ్ ఓపెన్ మే 22 నుంచి జూన్ 11 వరకు జరుగుతుంది. డబుల్స్ పార్ట్ నర్ బార్బొరా స్ట్రికోవాతో కలిసి ఆస్ట్రేలియన్ ఓపెన్ కోసం రెడీ అవుతోంది.
కెరియర్ స్లామ్ సాధించడం మినహా జీవితంలో పెద్ద కోరిక మరేమీ లేదని చెబుతోంది సానియా. ఫ్రెంచ్ ఓపెన్ లో కూడా బార్బొరాతోనే కలిసి ఆడతానని, పార్ట్ నర్ ను మార్చే ఆలోచన లేదని తెలిపింది. మార్టినా హింగిస్ తో కలిసి నెంబర్ వన్ గా నిలిచానని, ఆమె అద్భుతమైన క్రీడాకారిణి అని కితాబిచ్చింది. ఐతే బార్బొరా తనకు బాగా తెలుసునని, 14 ఏళ్ల వయసులోనే ఇద్దరూ కలిసి ఆడామని సానియా చెప్పింది. ఇక మిక్స్ డ్ డబుల్స్ పార్ట్ నర్ ఇవాన్ డాడిగ్ గాయంతో బాధపడుతున్నాడని , కోలుకున్న తర్వాతే అతడితో ఆడే విషయంపై మాట్లాడుతానంది.
చైనాలో సానియా తీన్మార్..
```


### Sangraha verified — Kannada

- **S3 key:** `datasets/sangraha/verified/kan/data-0.parquet`
- **Column:** `text`
- **Document id:** `595897c4b635c3c4d05565f311d161e1d73ec99a` (column `doc_id`)
- **Character length:** 832

```
ನಗರದ ಕುಮಾರಸ್ವಾಮಿ ದೇವಸ್ಥಾನದ ಮುಖ್ಯರಸ್ತೆ ಬಳಿ ಇರುವ ಕುರುಬರ ಸಂಘದ ಆವರಣದಲ್ಲಿ ವಸತಿ ನಿಲಯ ಕಟ್ಟಡ ನಿರ್ಮಾಣಕ್ಕಾಗಿ ಅಗೆದಿದ್ದ ಅಂದಾಜು 10 ಅಡಿ ಆಳದ ಬುನಾದಿಯಲ್ಲಿ ಬಿದ್ದ ಹೋರಿಯನ್ನು ಅಗ್ನಿಶಾಮಕದಳ ಸಿಬ್ಬಂದಿ ಭಾನುವಾರ ರಕ್ಷಿಸಿದರು.
 ಬಳ್ಳಾರಿ : ನಗರದ ಕುಮಾರಸ್ವಾಮಿ ದೇವಸ್ಥಾನದ ಮುಖ್ಯರಸ್ತೆ ಬಳಿ ಇರುವ ಕುರುಬರ ಸಂಘದ ಆವರಣದಲ್ಲಿ ವಸತಿ ನಿಲಯ ಕಟ್ಟಡ ನಿರ್ಮಾಣಕ್ಕಾಗಿ ಅಗೆದಿದ್ದ ಅಂದಾಜು 10 ಅಡಿ ಆಳದ ಬುನಾದಿಯಲ್ಲಿ ಬಿದ್ದ ಹೋರಿಯನ್ನು ಅಗ್ನಿಶಾಮಕದಳ ಸಿಬ್ಬಂದಿ ಭಾನುವಾರ ರಕ್ಷಿಸಿದರು.
 ವಸತಿ ನಿಲಯ ಹಾಗೂ ವಾಣಿಜ್ಯ ಸಂಕೀರ್ಣ ಕಟ್ಟಡ ನಿರ್ಮಿಸಲು ಆಳ ಮತ್ತು ಅಗಲವಾದ ಬುನಾದಿಯನ್ನು ತೋಡಲಾಗಿದೆ. ಮೇವು ಅರಸಿ ಬಂದ ಆ ಹೋರಿಯು ದಿಢೀರ್ ಬುನಾದಿ ಗುಂಡಿಯ ಆಳಕ್ಕೆ ಬಿದ್ದಿದೆ. ಕೆಲಕಾಲ ತನ್ನಷ್ಟಕ್ಕೆ ತಾನೇ ಮೇಲೇರಲು ಹರಸಾಹಸ ಪಟ್ಟಿದೆ. ಮೂಕ ಪ್ರಾಣಿಯ ರೋದನೆ ಕಂಡು ಮಮ್ಮಲ ಮರಗಿದ ಸಾರ್ವಜನಿಕರು ಕೂಡಲೇ ಅಗ್ನಿಶಾಮಕ ದಳ ಸಿಬ್ಬಂದಿಗೆ ವಿಷಯ ತಿಳಿಸಿದ್ದಾರೆ.
 ವಿಷಯ ತಿಳಿಯುತ್ತಿದ್ದಂತೆಯೇ ಸ್ಥಳಕ್ಕೆ ಧಾವಿಸಿದ ಅಗ್ನಿಶಾಮಕ ದಳ ಸಿಬ್ಬಂದಿ ಹಾಗೂ ಸಾರ್ವಜನಿಕರು ಗುಂಡಿಯ ಆಳದಲ್ಲಿದ್ದ ಹೋರಿಯನ್ನು ಪೈಪ್ ಸಹಾಯದೊಂದಿಗೆ ಮೇಲೆತ್ತಿದರು. 
```


### Sangraha verified — Marathi

- **S3 key:** `datasets/sangraha/verified/mar/data-0.parquet`
- **Column:** `text`
- **Document id:** `4603f789ccfb42194bea07a0dd5c30940fb8c592` (column `doc_id`)
- **Character length:** 2,522

The first 700 characters, then the last 700. 1,122 characters were cut from the middle.

```
शासनाने प्रादेशिक योजनेतील गावांना पाणीपुरवठा होत नसल्याने विद्युत व तांत्रिक प्रस्ताव मागविले असून यापूर्वीच्या रखडलेल्या वीजदेयकांची अदायगी करण्याचा विचार करीत आहे. हिंगोली जि. प. ने सिद्धेश्वर, पुरजळ व मोरवाडी योजनेचे प्रस्ताव यात पाठविल्याची माहिती मुख्य कार्यकारी अधिकारी एच. पी. तुम्मोड यांनी दिली.
 हिंगोली : शासनाने प्रादेशिक योजनेतील गावांना पाणीपुरवठा होत नसल्याने विद्युत व तांत्रिक प्रस्ताव मागविले असून यापूर्वीच्या रखडलेल्या वीजदेयकांची अदायगी करण्याचा विचार करीत आहे. हिंगोली जि. प. ने सिद्धेश्वर, पुरजळ व मोरवाडी योजनेचे प्रस्ताव यात पाठविल्याची माहिती मुख्य कार्यकारी अधिकारी एच. पी. तुम्मोड यांनी दिली.
 जिल्हा परिषदेत आज पाणीपुरवठा योजनांचा आढावा तुम्मोड यांनी घेतला. यावेळी त्यांन
```


1,122 characters cut

```
वी, असेही सांगितले.
 भौतिकदृष्ट्या पूर्ण मात्र आर्थिकदृष्ट्या अपूर्ण असलेल्या १0७ पैकी १0 योजनांची कामे पूर्ण झाली आहेत. तर आणखी ३0 प्रकरणे जि. प. त दाखल झाली आहेत. उर्वरित ६७ योजनांची कामे प्राधान्याने पूर्ण करून संबंधितांची देयके अदा करण्यास सांगितले. अपूर्ण असलेल्या २५ योजनांमुळे ही गावे टंचाईतही येत आहेत अन् या योजनांवर झालेला खर्चही वाया जात आहे. त्यामुळे या योजनांवर आधी लक्ष केंद्रित करून त्या पूर्ण कशा होतील, याचे अभियंतानिहाय नियोजन करण्यास सांगितले. तर यापैकी ३ योजना पूर्ण झाल्याचे सांगण्यात आले.
 अधिग्रहणाचे प्रस्ताव आता ज्या दिवशी पाणीपुरवठा सुरू झाला त्या दिवसापासूनच मंजूर होणार असल्याने तसे शेतकऱ्यांना सांगून अधिग्रहणास विलंब लागणार नाही, याची काळजी घेण्यासही तुम्मोड सांगितले. 
```


### Sangraha verified — Gujarati

- **S3 key:** `datasets/sangraha/verified/guj/data-0.parquet`
- **Column:** `text`
- **Document id:** `8607767fdf19be67d86ceba5a6d51fad936d5d55` (column `doc_id`)
- **Character length:** 2,202

The first 700 characters, then the last 700. 802 characters were cut from the middle.

```
જામનગર :
જામનગર જિલ્લામાં ડામર ચોરીના કૌભાંડમાં પીએસઆઈનો પુત્ર રંગહાથે ઝડપાઈ જતાં ચકચાર મચી જવા પામી હતી. જોડીયાના ભાદરા પાસે ડામર ચોરીનું કૌભાડ ઉજાગર થવા પામ્યું હતું. એક મહિના સુધી ચાલી રહેલા આ ડામર ચોરીના કૌભાડની ગંભીરતાને ધ્યાને લઈ તપાસ એલ.સી.બી.ને સોપવામાં આવી છે. અને જે વિસ્તારમાં કૌભાંડ એક મહિનાથી ધમધમતું હતું, તે એરિયાના પોલીસ સ્ટેશનના પીએસઆઈ એલ.ડી. ઓડેદરાને ફરજમાં બેદરકારી બદલ જિલ્લા પોલીસ વડાએ સસ્પેન્ડ કરી દીધા છે. આ ઉપરાંત આ મામલે રંગહાથે પકડાયેલા આરોપી પીએસઆઈના પુત્ર યુવરાજસિંહને કોર્ટમાં 14 દિવસની રિમાન્ડની માંગણી સાથે રજૂ કરતા કોર્ટે તેના 5 દિવસના રિમાન્ડ મંજૂર કર્યા હતા.
નવી દિલ્હી :
સુરત રેપ કેસમાં બે મહીનાથી ફરાર આસારામનો પુત્ર નારાયણ સાંઈ આખરે પોલીસના હાથે ઝડપાયો છે. પોલીસે
```


802 characters cut

```
્વિક નેતાઓ, ઉદ્યોગપતિઓ અને સેલિબ્રિટીનું નામનું શોર્ટલિસ્ટ કર્યું છે. વિજેતાના નામનું એલાન હવેના મહીનામાં કરવામાં આવશે.
નવી દિલ્હી :
દેશની સૌથી મોટી મર્ડર મિસ્ટ્રી આરૂષિ હેમરાજ હત્યાકાંડમાં આજે સાડા પાંચ વર્ષ પછી આખરે નિર્ણય આવવાનો છે. આ બે હત્યાકાંડમાં ગાઝિયાબાદની વિશેષ સીબીઆઈ અદાલત આજે નિર્ણય આપશે.
આગ્રા :
ભારતીય જનતા પાર્ટીના પ્રધાનમંત્રી પદના ઉમેદવાર નરેન્દ્ર મોદી એક સમયે મુગલોની રાજધાની રહી ચૂકેલી તાજનગરી આગ્રામાં આજે રેલીનું સંબોધન કરશે. આગ્રામાં મોદીની રેલીને લઈને ભાજપના સમર્થકોની વચ્ચે ભારે ઉત્સાહ દેખાઈ રહ્યો છે. રેલીમાં 40 વિધાનસભા ક્ષેત્રો અને આઠ લોકસભા વિસ્તારમાંથી લોકો રેલીમાં સામેલ થવાનો દાવો કરવામાં આવી રહ્યો છે. રેલી માટે તૈયારીને બુધવારે મોડી રાત સુધી અંતિમ ઓપ આપવામાં આવ્યો.
```


### Sangraha synthetic — Hindi

- **S3 key:** `datasets/sangraha/synthetic/hin_Deva/wiki_hin_Deva_0000_of_0063.parquet`
- **Column:** `text`
- **Document id:** `e67b36720d16f52a049bab2252b1a6f8cd02fe131140dc38e23a00e8f0e71ed8` (column `doc_id`)
- **Character length:** 907

```

मिनोलिया गिलवोस्प्लेंडेंस

मिनोलिया गिलवोस्प्लेंडेंस समुद्री घोंघे की एक प्रजाति है, जो सोलारीलिडे परिवार में एक समुद्री गैस्ट्रॉपोड मोलस्क है।
वर्णन।
खोल की ऊँचाई 6.5 मिमी और इसका व्यास 8 मिमी हो जाता है। चमकते, हल्के-सफेद खोल का आकार शंक्वाकार होता है और यह गहराई से नाभि वाला होता है। खोल में पाँच चक्कर होते हैं। छिद्र रैखिक है। स्तंभाकार सीमा कोने में संक्षेप में परिलक्षित होती है।
घूर्णन चिकने होते हैं, टांकों पर चैनल किए जाते हैं, उनके ठीक नीचे उभरे हुए राज्याभिषेक गांठों की एक पंक्ति के साथ अलंकृत होते हैं, जो बेसल घूर्णन के सामने कम अलग होते हैं-यह भौतिक रूप से खोल को थोड़ा कोण वाला रूप देने में सहायता करता है। यह सफेद है, जिसमें कई लौ जैसे निशान हैं। नाभि गहरी होती है और बहुत कम सिकुड़ जाती है। नाभि को स्वयं एक अनुप्रस्थ-चैनल वाली मूर्ति से सजाया गया है। इसका पदार्थ मार्जरीटेसियस है। गोल और सरल छिद्र का आंतरिक भाग मोती और चिकना है।
वितरण।
समुद्री प्रजातियाँ फिलीपींस में पाई जाती हैं।

```


### Sangraha synthetic — Bengali

- **S3 key:** `datasets/sangraha/synthetic/ben_Beng/wiki_ben_Beng_0000_of_0063.parquet`
- **Column:** `text`
- **Document id:** `d394e108f5bf20d45723671346e546a74c5e0d018bd762bdd0bcf9e2bde86dbd` (column `doc_id`)
- **Character length:** 449

```

তুহামি ঘেজ্জুল

তুহামি ঘেজুল (জন্ম 5 জানুয়ারি 1987) একজন আলজেরিয়ান বাস্কেটবল খেলোয়াড় যিনি সিরিয়ান বাস্কেটবল লিগের আল-কারামার হয়ে খেলেন। তিনি জিএস পেট্রোলিয়ার্সের হয়েও খেলেছেন। 
পেশাগত কর্মজীবন।
আল নাসরের সঙ্গে তাঁর কর্মজীবন শুরু করেন ঘেজুল। 2011 সালে, তিনি জিএস পেট্রোলিয়ার্সের সাথে চুক্তিবদ্ধ হন যেখানে তিনি তখন থেকেই খেলে আসছেন।
2022 সালের 6ই মে, শেষ চার ধাপের আগে সিরিয়ান বাস্কেটবল লিগের (এসবিএল) আল-কারামার সাথে গেজুল স্বাক্ষর করেন।

```


### Sangraha synthetic — Tamil

- **S3 key:** `datasets/sangraha/synthetic/tam_Taml/wiki_tam_Taml_0000_of_0063.parquet`
- **Column:** `text`
- **Document id:** `51de8796c4be8c1ea33e191ea6374f21420777f4cf9f6b700ee4ef46df5135d2` (column `doc_id`)
- **Character length:** 3,020

The first 700 characters, then the last 700. 1,620 characters were cut from the middle.

```

ஃபுராஸாபோல்

ஃபராஸாபோல் (,) (பிராண்ட் பெயர்கள் ஃப்ராஸலான், மியோடலான், கு ஜி ஷூ), ஆண்ட்ரோஃபுரசானால் என்றும் அழைக்கப்படுகிறது, இது ஒரு செயற்கை, வாய்வழி செயலில் உள்ள அனபோலிக்-ஆண்ட்ரோஜெனிக் ஸ்டீராய்டு ஆகும், இது 1969 முதல் ஜப்பானில் சந்தைப்படுத்தப்பட்டுள்ளது. இது டைஹைட்ரோடெஸ்டோஸ்டிரோனின் (டிஎச்டி) 17α-ஆல்கைலேட்டட் வழித்தோன்றல் ஆகும், மேலும் இது ஸ்டானோசோலுடன் கட்டமைப்பு ரீதியாக நெருக்கமாக தொடர்புடையது, இது பைரசோலுக்கு பதிலாக ஒரு ஃபராஸன் வளைய அமைப்பைக் கொண்டிருப்பதன் மூலம் மட்டுமே வேறுபடுகிறது. ஃபுராஸாபோல் அனபோலிக் மற்றும் ஆண்ட்ரோஜெனிக் செயல்பாட்டின் ஒப்பீட்டளவில் அதிக விகிதத்தைக் கொண்டுள்ளது. மற்ற 17α-ஆல்கைலேட்டட் ஆச்களைப் போலவே, இது ஹெபடோடாக்ஸிஸிட்டி அபாயத்தைக் கொண்டிருக்கலாம். இந்த மருந்து ஒரு
```


1,620 characters cut

```
ன் ஒரு மாதத்திற்குள் சுயமாக நிர்வகிக்கப்பட்ட ஸ்டானோசோலோல் என்று கூறினார்.
பின்னர் ஜான்சனின் பயிற்சி துணையான ஆஞ்செல்லா இசாஜென்கோ, அவரும் அஸ்டாபானிடமிருந்து ஃபுராஸாபோல் பெற்றதாக ஆணையத்திடம் கூறினார், அல்லது அவள் நினைத்தாள். முன்னாள் கனடிய சாதனையாளர், ஜான்சனின் நேர்மறையான சோதனையின் பின்னர், ஃபுராஸாபோல் இருப்பதாக அவர் நினைத்த ஒரு எஞ்சிய குப்பியில் அவர் ஒரு பகுப்பாய்வு செய்ததாகவும், அது ஸ்டானோசோலோல் என்று அடையாளம் காணப்பட்டதாகவும் தெரியவந்தது. இசாஜென்கோவும், பின்னர் ஆணையத்தின் தலைமை நீதிபதி சார்லஸ் டூபினும், அஸ்டாபன் ஜான்சன், இசாஜென்கோ மற்றும் பிற கனடிய குழு உறுப்பினர்களிடம் ஸ்டானோசோலோலை செலுத்தியதாகவும், ஃபுராஸாபோல் அவரது கற்பனையின் ஒரு உருவம் அல்லது ஒரு முழுமையான பொய் என்றும் முடிவு செய்தனர்.

```


### Sangraha synthetic — Telugu

- **S3 key:** `datasets/sangraha/synthetic/tel_Telu/wiki_tel_Telu_0000_of_0063.parquet`
- **Column:** `text`
- **Document id:** `3829f131e61846f85b4910a854c2457460054931e864206a7391ab87ca254b5c` (column `doc_id`)
- **Character length:** 366

```

టైర్ సిటీ మ్యూజియం

టైర్ సిటీ మ్యూజియం టర్కీలోని ఇజ్మిర్ ప్రావిన్స్లోని టైర్ ఇల్సే (జిల్లా) లో ఉంది. ఈ భవనం గతంలో టైర్ యొక్క సిటీ హాల్. ఇది 1955లో నిర్మించబడింది. మునిసిపాలిటీ కోసం కొత్త భవనం నిర్మించిన తరువాత, మునుపటి భవనం పునరుద్ధరించబడింది మరియు 15 అక్టోబర్ 2014న టైర్ సిటీ మ్యూజియంగా ప్రారంభించబడింది.
విభాగాలు.
మ్యూజియంలోని విభాగాలు ఈ క్రింది విధంగా ఉన్నాయిః

```


### Sangraha synthetic — Kannada

- **S3 key:** `datasets/sangraha/synthetic/kan_Knda/wiki_kan_Knda_0000_of_0063.parquet`
- **Column:** `text`
- **Document id:** `1e7807344a489d897f8d46588c3ee20ebcbaf5f1d5398b1b5b514b0283b28652` (column `doc_id`)
- **Character length:** 2,237

The first 700 characters, then the last 700. 837 characters were cut from the middle.

```

ಸಿಸಿರಿಂಚಿಯಂ ಡೈಕೋಟೋಮಮ್

ಸಿಸಿರಿಂಚಿಯಂ ಡೈಕೋಟೋಮಮ್ ಎಂಬುದು ಐರಿಸ್ ಕುಟುಂಬದ ಅಪರೂಪದ ಹೂಬಿಡುವ ಸಸ್ಯವಾಗಿದ್ದು, ಇದನ್ನು ಸಾಮಾನ್ಯ ಹೆಸರುಗಳಾದ ವಿಷ್ಬೋನ್ ಬ್ಲೂ-ಐಡ್ ಹುಲ್ಲು, ವೈಟ್ ಐರಿಸೆಟ್ ಮತ್ತು ರಿಫ್ಲೆಕ್ಸ್ಡ್ ಬ್ಲೂ-ಐಡ್ ಹುಲ್ಲು ಎಂದು ಕರೆಯಲಾಗುತ್ತದೆ. ಇದು ಯುನೈಟೆಡ್ ಸ್ಟೇಟ್ಸ್ನ ಉತ್ತರ ಕೆರೊಲಿನಾ ಮತ್ತು ದಕ್ಷಿಣ ಕೆರೊಲಿನಾಕ್ಕೆ ಸ್ಥಳೀಯವಾಗಿದೆ, ಅಲ್ಲಿ ನಾಲ್ಕು ಕೌಂಟಿಗಳಲ್ಲಿ ಹತ್ತಕ್ಕಿಂತ ಕಡಿಮೆ ಜನಸಂಖ್ಯೆ ಉಳಿದಿದೆ. ಇದು ತನ್ನ ಆವಾಸಸ್ಥಾನದ ನಷ್ಟ ಮತ್ತು ಅವನತಿಗೆ ಅಪಾಯಕಾರಿಯಾಗಿದೆ ಮತ್ತು ಸಂಯುಕ್ತ ಸಂಸ್ಥಾನದ ಒಕ್ಕೂಟದ ಪಟ್ಟಿ ಮಾಡಲಾದ ಅಳಿವಿನಂಚಿನಲ್ಲಿರುವ ಪ್ರಭೇದವಾಗಿದೆ.
ಈ ಸಸ್ಯವು ಹುಲ್ಲಿನಂತಹ ಎಲೆಗಳೊಂದಿಗೆ 40 ಸೆಂಟಿಮೀಟರ್ ಎತ್ತರದ ಕವಲೊಡೆಯುವ ಕಾಂಡಗಳ ಗುಂಪನ್ನು ಉತ್ಪಾದಿಸುವ ಒಂದು ದೀರ್ಘಕಾಲಿಕ ಮೂಲಿಕೆಯಾಗಿದೆ. ಏಕಾಂಗಿ ಹೂವು ಹಳದಿ ತಳಗಳನ್ನು ಹೊಂದಿರುವ ಆರು ಬಿಳಿ ತೆಪ್ಪಗಳನ್ನು ಹೊಂದಿದ್ದು, ಪ್ರತಿಯೊಂದೂ 0.75 ಸೆಂಟಿಮೀಟರ್ಗಳಷ್
```


837 characters cut

```
ತರ ಸಮಸ್ಯೆಗಳನ್ನು ಎದುರಿಸುತ್ತಿದೆ, ಇದರಲ್ಲಿ ಕುಡ್ಜು ("ಪುಯೆರಿಯಾ ಲೋಬಾಟಾ") "ದಕ್ಷಿಣವನ್ನು ತಿನ್ನುವ ಬಳ್ಳಿ", ಜಪಾನೀಸ್ ಹನಿಸಕಲ್ ("ಲೋನಿಕೆರಾ ಜಪೋನಿಕಾ"), ಮತ್ತು ನೇಪಾಳದ ಬ್ರೌನ್ ಟಾಪ್ ("ಮೈಕ್ರೊಸ್ಟೆಜಿಯಂ ವಿಮಿನಿಯಂ") ನಂತಹ ಪರಿಚಯಿಸಲಾದ ಸಸ್ಯಗಳ ಪ್ರಭೇದಗಳ ಆಕ್ರಮಣದಿಂದ ಅದರ ಆವಾಸಸ್ಥಾನವನ್ನು ವಶಪಡಿಸಿಕೊಳ್ಳಲಾಗಿದೆ. ಸಸ್ಯವು ತನ್ನ ಆವಾಸಸ್ಥಾನದಲ್ಲಿನ ಅಡಚಣೆಯ ಸಮಯದಲ್ಲಿ ಹಾನಿಗೊಳಗಾಗಬಹುದಾದರೂ, ಕಾಡ್ಗಿಚ್ಚಿನಂತಹ ಕೆಲವು ನೈಸರ್ಗಿಕ ರೀತಿಯ ಅಡಚಣೆಗಳಿಗೆ ಇದು ಹೊಂದಿಕೊಳ್ಳುತ್ತದೆ. ನೈಸರ್ಗಿಕ ಅಗ್ನಿ ವ್ಯವಸ್ಥೆಯು ಸಸ್ಯಕ್ಕೆ ಅಗತ್ಯವಿರುವ ತೆರೆದ ತೆರವು ಮತ್ತು ತೆಳುವಾದ ಕಸದ ಪದರವನ್ನು ನಿರ್ವಹಿಸುತ್ತದೆ. ಇತರ ಅಪಾಯಗಳಲ್ಲಿ ಸಸ್ಯನಾಶಕಗಳ ಬಳಕೆ ಮತ್ತು ಸವೆತ ಸೇರಿವೆ.
ಈ ಸಸ್ಯವನ್ನು ಇತ್ತೀಚೆಗೆ 1942ರಲ್ಲಿ "ಸಾಕಷ್ಟು ಸಾಮಾನ್ಯ" ಎಂದು ಪರಿಗಣಿಸಲಾಗಿದ್ದರೂ, ಮಾನವ ಚಟುವಟಿಕೆಯು ಅದರ ವ್ಯಾಪ್ತಿಯಾದ್ಯಂತ ಅದರ ಆವಾಸಸ್ಥಾನವನ್ನು ಸೂಕ್ತವಲ್ಲದಂತಿಸಿದೆ.

```


### Sangraha synthetic — Marathi

- **S3 key:** `datasets/sangraha/synthetic/mar_Deva/wiki_mar_Deva_0000_of_0063.parquet`
- **Column:** `text`
- **Document id:** `c81b7844d851792a160a00b8735b079cb6347cb9d89b7172325e612d733288c7` (column `doc_id`)
- **Character length:** 1,031

```

अपघातीपणा (तत्त्वज्ञान)

तत्त्वज्ञानात, अपघातीपणा हा भौतिक निर्धारवादाचे कारणात्मक समापन नाकारतो आणि असे सांगतो की घटना एकमेकांमध्ये अव्यवस्थितपणे किंवा योगायोगाने यशस्वी होऊ शकतात (गणितीयदृष्ट्या नव्हे तर लोकप्रिय अर्थाने). अपघातीतेच्या विरोधकांचे म्हणणे आहे की जे एक आकस्मिक घटना असल्याचे दिसते ते प्रत्यक्षात एक किंवा अधिक कारणांचा परिणाम आहे जे केवळ तपासाच्या अभावामुळे अज्ञात राहते. चार्ल्स सँडर्स पियर्से यांनी विश्वाच्या प्रक्रियेत संधीला वस्तुनिष्ठ घटक बनविणाऱ्या सिद्धांतांसाठी टायचिझम (τüχη, संधी) ही संज्ञा वापरली.
नैतिकतेत ही संज्ञा, अनिश्चिततेप्रमाणेच, मानसिक बदलाचे श्रेय नेहमी पूर्वी निश्चित केलेल्या मानसिक अवस्थांशी दिले जाऊ शकत नाही आणि ती इच्छाशक्ती कारणास्तव त्यात समाविष्ट असलेल्या हेतूंशी संबंधित नाही हा सिद्धांत दर्शविण्यासाठी वापरली जाते. या सिद्धांताचे एक उदाहरण म्हणजे 'लिबरम आर्बिट्रियम इंडिफरन्सी' ('उदासीनतेचे स्वातंत्र्य') हा सिद्धांत, ज्याच्या आधारे दोन किंवा अधिक पर्यायी शक्यतांच्या निवडीवर नैतिक किंवा विवेकपूर्ण प्रकारच्या समकालीन माहितीचा किंवा स्फटिकीकृत सवयीचा (चारित्र्य) परिणाम होत नाही.

```


### Sangraha synthetic — Gujarati

- **S3 key:** `datasets/sangraha/synthetic/guj_Gujr/wiki_guj_Gujr_0000_of_0063.parquet`
- **Column:** `text`
- **Document id:** `5a98810323410c20655e68ae21f5d4f5e55d9e56e33d83be6442d74834df8642` (column `doc_id`)
- **Character length:** 4,278

The first 700 characters, then the last 700. 2,878 characters were cut from the middle.

```

આર્ચી ગિપ્સ

આર્ચી ગિપ્સ એક અમેરિકન ફિલ્મ નિર્માતા અને નિર્માતા છે, જેનો ઉછેર ન્યૂ યોર્કના રોશેલમાં થયો છે, જે લોસ એન્જેલિસમાં રહે છે. તેઓ અવાસ્તવિક વિચારોના સહસ્થાપક અને ભાગીદાર/પ્રમુખ છે, એક ઉત્પાદન કંપની જે બિન-વર્ણનાત્મક સ્વરૂપોમાં નિષ્ણાત છે. તેના ભાગીદારો માર્ક વાહલબર્ગ અને સ્ટીફન લેવિન્સન છે.
પ્રારંભિક જીવન.
ગિપ્સે શિકાગો જતા પહેલા સિરાક્યુઝ યુનિવર્સિટીમાં પ્રસારણ પત્રકારત્વનો અભ્યાસ કર્યો હતો.
જ્યાં તેમણે બીજા શહેરમાં તાલીમ લીધી હતી અને ઘણા નાટકો અને સ્કેચ લખ્યા હતા.
કોમેડી રીવ્યુ "સેટરડે મોર્નિંગ લાઇવ" સહિત શો. તેમણે ન્યૂયોર્ક યુનિવર્સિટીની ટિશ સ્કૂલ ઓફ ધ આર્ટ્સમાંથી ફિલ્મમાં અનુસ્નાતક મેળવ્યું હતું, જ્યાં તેમણે શ્રેષ્ઠ હાસ્ય પટકથા માટે ટોચના સ્નાતક પટકથા લેખક વિદ્યાર્થી પુરસ્કાર અ
```


2,878 characters cut

```
ક્ઝિક્યુટિવે અવાસ્તવિક વિચારો દ્વારા ઘણા પ્રોજેક્ટનું નિર્માણ કર્યું છે, જેમાં હિટ એચ. બી. ઓ. ટ્રુ ક્રાઈમ લિમિટેડ દસ્તાવેજી શ્રેણી, એમ. સી. મિલિયન્સ, રોકુઝ રન આ સિટી, એચ. બી. ઓ. એસ. ધ મર્ડર એટ સ્ટાવર્ડ રોક અને એચ. બી. ઓ. મેક્સ વાહ્લ સ્ટ્રીટનો સમાવેશ થાય છે, જેમાં તે કેમેરા પર પણ દેખાય છે. ગિપ્સને એમ. મિલિયન્સ માટે ઉત્કૃષ્ટ દસ્તાવેજી અથવા નોનફિક્શન શ્રેણી માટે એમી એવોર્ડ માટે નામાંકિત કરવામાં આવ્યા હતા, વાહલ સ્ટ્રીટ માટે શ્રેષ્ઠ બિઝનેસ શો માટે વિવેચકની પસંદગીનો વાસ્તવિક ટીવી એવોર્ડ, આ શહેર ચલાવવા માટે શ્રેષ્ઠ ટૂંકા સ્વરૂપ શ્રેણી માટે ઇડા દસ્તાવેજી એવોર્ડ અને સ્ટારવેડ રોક ખાતે હત્યાઓ માટે ઉત્કૃષ્ટ ગુના અને ન્યાય દસ્તાવેજી માટે સમાચાર અને દસ્તાવેજી એમી એવોર્ડ માટે નામાંકિત કરવામાં આવ્યા હતા. 

```


### Sangraha unverified — Hindi

- **S3 key:** `datasets/sangraha/unverified/hin/data-0.parquet`
- **Column:** `text`
- **Document id:** `7d54e80b012eacaba53561c1e4a3311299c403481b12b2037c6b42f0a65acd57` (column `doc_id`)
- **Character length:** 1,355

```
बनारस से प्रकाशित "पूर्वांचल आजकल" के बंद होने की चर्चा । No. 1 Indian Media News Portal\nबनारस से प्रकाशित "पूर्वांचल आजकल" के बंद होने की चर्चा\nबनारस से प्रकाशित सांध्य दैनिक के बंद होने की चर्चाएं हैं. अखबार पिछले कुछ दिनों से शहर में नहीं दिख रहा है. कई दिनों से अखबार लोगों को पढ़ने को भी नहीं मिला है, जिसके चलते लोग कयास लगा रहे हैं कि अखबार बंद होने जा रहा है. पांच महीने पहले शुरू हुए इस सांध्य दैनिक ने शहर में अपनी एक अच्छी पहचान बना ली है. बनारस में लोगों को गांडीव की बजाय पूर्वांचल आजकल का इंतजार रहने लगा है. लिहाजा इसका मार्केट में न आना इसके बंद होने की कयास को जन्म दे रहा है. साथ ही इस अखबार के साथ जुड़े पत्रकार भी अपने भविष्य को लेकर चिंतित नजर आ रहे हैं.\nइस अखबार का संपादन बनारस के वरिष्ठ पत्रकार डा. राधारमण चित्रांशी कर रहे हैं. डा. चित्रांशी पिछले तीन दशक से ज्यादा समय से बनारस की पत्रकारिता में सक्रिय हैं. बनारस के प्रमुख सांध्य दैनिक गांडीव से इस्तीफा देने के बाद उन्होंने इस अखबार का प्रकाशन शुरू किया. अखबार बंद होने के सवाल को पूरी तरह नकारते हुए डा. चित्रांशी कहते हैं कि यह अफवाह बनारस में मौजूद एक काकस फैला रहा है. अखबार बंद होने नहीं जा रहा है. वे कहते हैं कि जिस प्रेस से अखबार का प्रकाशन कराया जाता था, वहां मशीन में गड़बड़ी के चलते अखबार का व्यापारिक प्रकाशन नहीं हो पा रहा है. कम से कम एक सप्ताह लगेगा इस स्थिति को ठीक होने में, इसलिए हम सिर्फ ऑफिस कापी छपवा रहे हैं. इसके बंद होने की सूचना बिल्कुल निराधार है.
```


### Sangraha unverified — Bengali

- **S3 key:** `datasets/sangraha/unverified/ben/data-0.parquet`
- **Column:** `text`
- **Document id:** `30138a045a2dc323917de00e0acc981df3810d5275ba0b25f6a3ebb7879665ef` (column `doc_id`)
- **Character length:** 4,489

The first 700 characters, then the last 700. 3,089 characters were cut from the middle.

```
০	নিউজ ডেস্কঃ সিলেটের দক্ষিণ সুরমার কাজী পরিবারের 'দুই কইন্যা' এখন বড় অসহায়। একই গোষ্ঠীর স্বজনদের ক্রমাগত হুমকির কারণে মৃত্যু তাড়া করে ফিরছে তাদের। ইতিমধ্যে তাদের উপর হয়েছে হামলা। গোষ্ঠীর পাঁচের বাদ করে রাখায় এখন পাড়ার মক্তরে তাদের যাওয়া-আসাও বন্ধ। রাস্তায় বের হলেই তারা থাকেন হামলার তটস্থে। সিলেটের দক্ষিণ সুরমার কাজী পরিবারের ওই দুই বোনের নাম কাজী সুলতানা ও কাজী ইয়াসমীন।
গতকাল সিলেটে সংবাদ সম্মেলনে দুই বোন তাদের দুঃখের কথা জানিয়েছেন। সহায়তা চান প্রশাসনসহ সাংবাদিকদের। বলেন, স্বাধীনতাবিরোধী একটি রাজনৈতিক দলের ছায়ায় থাকা ওই চক্রের সদস্যরা তাদের ফলো করছে। যে কোনো সময় তারা হামলায় মারাও যেতে পারেন। ঘটনার সূত্রপাত প্রায় ৮ বছর আগে। ২০০৮ সালে। কাজী সালমার ছোটো বোন কাজী ইয়াসমীনের বিয়
```


3,089 characters cut

```
অভিযোগ করা হয়েছে। বোন কাজী ইয়াসমিন ২০১৫ সালের ১৫ই নভেম্বরে জীবনের নিরাপত্তা ও পাওনা টাকা উদ্ধারে পুলিশ কমিশনার বরাবরে অভিযোগ দেন। পরে বিষয়টি এলাকার লোকজন মিলে নিষ্পত্তি করেন। কিন্তু দীর্ঘদিন পর আবার তারা উৎপাত শুরু করে। বর্তমানে তাকেসহ ছোট বোনের স্বামী কবির উদ্দিন, বড় ভাই কাজী ডালিমকে মামলায় জড়ানোর চেষ্টা করছে। যে কোনো সময় আসামিরা আবার হামলা-মামলা দিয়ে হয়রানি করতে পারে। কাজী ইয়াসমীন মানবজমিনকে জানিয়েছেন, 'আমি বিয়ে করেছি নিজের ইচ্ছায়।
আমাদের দু'টি পরিবারে সম্পর্কের কোনো অবনতি ঘটেনি। বরং আমরা সুখে আছি। কিন্তু আমার গোষ্ঠীর চাচারা পিছু ছাড়ছে না।' তিনি বলেন, 'ওরা জামায়াত-শিবির করে। ক্রমাগত হুমকির কারণে তটস্থ অবস্থায় আছি। কিন্তু তাদের উপর মামলা সত্ত্ব্বেও পুলিশ গ্রেপ্তার করছে না।'
```


### Sangraha unverified — Tamil

- **S3 key:** `datasets/sangraha/unverified/tam/data-0.parquet`
- **Column:** `text`
- **Document id:** `f2d56975c89e85cb3cd7c02cb67e706ce325d68a585cb7b2899bb6da8b643b3b` (column `doc_id`)
- **Character length:** 1,584

The first 700 characters, then the last 700. 184 characters were cut from the middle.

```
சிரியா மீதான தாக்குதல் ஏகாதிபத்திய இராணுவ அடக்குமுறையின் மற்றுமொரு கொடூரமான கட்டம்!
இறையாண்மை கொண்ட நாடான சிரியா மீதான கொடூரமான தாக்குதலை தாம் வன்மையாக கண்டிப்பதாக மக்கள் விடுதலை முன்னணி தெரிவித்துள்ளது.
ஐக்கிய அமெரிக்க, பிரித்தானியா மற்றும் பிரான்ஸ் ஆகிய நாடுகள் சேர்ந்து சிரியாவில் இரசாயன ஆயுதம் பயன்படுத்தியதாக குற்றச்சாட்டு முன்வைத்து சிரியா மீது அண்மையில் தாக்குதல் நடத்தப்பட்டது.
இதனை கண்டிக்கும் வகையில் மக்கள் விடுதலை முன்னணி வெளியிட்டுள்ள ஊடக அறிகையிலேயே மேற்கண்டவாறு தெரிவிக்கப்பட்டுள்ளது.
இரசாயன ஆயுத தாக்குதல் நடத்தப்பட்டதாக தெரிவிக்கப்படும் அறிக்கைகளை உறுதிப்படுத்த கூட நேரம் வழங்கப்படாமல் சிரியா மீது உடனடியாக தாக்குதல்கள் மேற்கொள்ளப்பட்டுள்ளதாக மக்கள் விடுதலை முன்னணி குற்றச்சாட்டியுள்
```


184 characters cut

```
்டுள்ளது.
"சிரியா மீதான தாக்குதலை நியாயப்படுத்துவதற்கு இரசாயன ஆயுத தாக்குதல் தொடர்பில் ஒரு கதையைப் பயன்படுத்தினாலும், இந்த நகர்வானது பல தசாப்தங்களாக அமெரிக்கா தலைமையிலான ஏகாதிபத்தியவாதிகளால் மேற்கொள்ளப்படும் அரசியல் மற்றும் இராணுவ ஆதிக்கத்தின் ஊடாக மத்திய கிழக்கு மற்றும் அது வழியாக எண்ணெய் இருப்பின் கட்டுப்பாட்டை கொண்டுவருவதற்கான நடவடிக்கை என்பது தெளிவானது." என அந்த அறிக்கையில் மேலும் குறிப்பிடப்பட்டுள்ளது.
சிரியா மீதான தாக்குதலை வன்மையாக கண்டிப்பதோடு, நாடுகளில் கைப்பொம்மை ஆட்சிகளை அமைப்பதன் ஊடாக நாடுகளை கைப்பற்றும் ஏகாதிபத்திய முயற்சிகளை தோற்கடிப்பதற்கு உலகெங்கிலுமுள்ள முற்போக்கான மக்களுக்கு அழைப்பு விடுப்பதாக, மக்கள் விடுதலை முன்னணி வெளியிட்டுள்ள ஊடக அறிக்கையில் மேலும் தெரிவிப்பட்டுள்ளது.
```


### Sangraha unverified — Telugu

- **S3 key:** `datasets/sangraha/unverified/tel/data-0.parquet`
- **Column:** `text`
- **Document id:** `d30d026a98be10aade8b103a135fdc764367cc543f607609f955452f9082081d` (column `doc_id`)
- **Character length:** 671

```
రజినీకాంత్ మోస్ట్ అవేటెడ్ మూవీ 2.0 టీజర్ రిలీజ్ డేట్ ఫిక్సయింది. రీసెంట్ గా ఆడియో రిలీజ్ జరుపుకున్న ఈ మూవీ ఏప్రియల్ లో రిలీజ్ కి రెడీ అవుతుంది. అయితే ఈ లోపు రిపబ్లిక్ డే సందర్భంగా జనవరి 26 న ఈ మూవీ టీజర్ ని రిలీజ్ చేసే ప్లాన్ లో ఉంది సినిమా యూనిట్.
ప్రస్తుతం ప్రీ ప్రొడక్షన్ ప్రాసెస్ లో ఉన్న ఈ సినిమా కోసం హాలీవుడ్ స్థాయి టెక్నీషయన్స్ తో గ్రాఫిక్ వర్క్ జరుగుతుంది. తెలుగు, తమిళ, హిందీ భాషలతో పాటు అరబిక్ భాషలోను రిలీజ్ కి రెడీ అవుతున్న ఈ సినిమాపై వరల్డ్ వైడ్ గా భారీ అంచనాలు సెట్ అయి ఉన్నాయి.
A.R. రెహమాన్ మ్యూజిక్ కంపోజ్ చేసిన ఈ సినిమాలో బాలీవుడ్ నటుడు అక్షయ్ కుమార్ విలన్ రోల్ ప్లే చేశాడు. రజినీకాంత్ సరసన ఎమీ జాక్సన్ హీరోయిన్ గా నటించింది. శంకర్ ఈ సినిమాకి డైరెక్టర్.
```


### Sangraha unverified — Kannada

- **S3 key:** `datasets/sangraha/unverified/kan/data-0.parquet`
- **Column:** `text`
- **Document id:** `3c9e300cfa98ee703cca3e86cc5cf79a5a6416c5447b450d9ef453b6efbdc3b6` (column `doc_id`)
- **Character length:** 2,821

The first 700 characters, then the last 700. 1,421 characters were cut from the middle.

```
Article-20180602.02.08 | Articles | ಸಮಾಜಮುಖಿ\nಗುಣಮಟ್ಟದ ಶಿಕ್ಷಣ ಮತ್ತು ಸಂಶೋಧನೆಯಲ್ಲಿ ಭಾರತದ ಸ್ಥಾನ ಏನು? ನಮ್ಮದೇ ಆದ ಹಾರ್ವರ್ಡ್ನ್ನು ನಾವು ಹೊಂದುವುದು ಯಾವಾಗ?\nಮೀಸಲು ಹಾಗೂ ಭ್ರಷ್ಟಾಚಾರದಿಂದಾಗಿ ಭಾರತದಲ್ಲಿ ವಿಶ್ವ ದರ್ಜೆಯ ಮೂರನೇ ಹಂತದ ಶೈಕ್ಷಣಿಕ ಸಂಸ್ಥೆಗಳು ಇಲ್ಲ. ಇದು ಸಾಮಾನ್ಯ ಅಭಿಪ್ರಾಯ. ಆದರೆ, ನಾವು ಹಾರ್ವರ್ಡ್ನಂಥ ವಿಶ್ವವಿದ್ಯಾನಿಲಯವನ್ನು ಭಾರತದಲ್ಲಿ ಸ್ಥಾಪಿಸಲು (ಸಧ್ಯದಲ್ಲಂತೂ ಆಗದ ಮಾತು!) ಏಕೆ ಸಾಧ್ಯವಾಗಿಲ್ಲ ಎನ್ನುವುದಕ್ಕೆ ಬೇರೆಯದೇ ಕಾರಣಗಳು ಇವೆ.\nಹಾರ್ವರ್ಡ್ ವಿಶ್ವವಿದ್ಯಾಲಯದ ವಾರ್ಷಿಕ ಬಜೆಟ್ 4.5 ಶತಕೋಟಿ ಡಾಲರ್(2015ರಲ್ಲಿ). ಇದರಲ್ಲಿ ಆಸಕ್ತರು ನೀಡುವ ಆರ್ಥಿಕ ನೆರವು ಹಾಗೂ ಹಳೆಯ ವಿದ್ಯಾರ್ಥಿಗಳು ನೀಡುವ ಅನುದಾನ ಸೇರ್ಪಡೆಗೊಂಡಿಲ್ಲ. 2017ರಲ್ಲಿ ಹಾರ್ವರ್ಡ್ ಪಡೆದ ದತ್ತಿ ಮೊತ್ತ 36 ಶತಕೋಟಿ ಡಾಲರ್. ಇದಕ್ಕೆ ತದ್ವಿರುದ್ಧವಾಗಿ 2018 - 19ನೇ ಸಾಲಿನಲ್ಲಿ ನಮ್ಮ ದೇಶದ ಎಲ್ಲ ಐಐಟಿ - ಐಐಎಂಗಳ ಒಟ್ಟು ವಾರ್ಷಿಕ ಬಜೆಟ್ 
```


1,421 characters cut

```
 ಸಾಧ್ಯವಾಗದೆ ಇರಲು ಇದೂ ಒಂದು ಕಾರಣ.\nಹಲವು ಶತಮಾನಗಳಿಂದ ಅಸ್ತಿತ್ವದಲ್ಲಿ ಇರುವುದರಿಂದ ಹಾರ್ವರ್ಡ್ನಂಥ ವಿಶ್ವವಿದ್ಯಾಲಯಗಳ ಕಾರ್ಯಜಾಲ ಮತ್ತು ವಿಶ್ವಸನೀಯತೆಯು ಅಗೋಚರವಾಗದ ಆದರೆ, ಕಡೆಗಣಿಸಲಾಗದ ಆಸ್ತಿಯಿದ್ದಂತೆ.\nಆಶಾವಾದದ ಯುಟೋಪಿಯನ್ ಕನಸುಗಳು ಏನೇ ಇರಲಿ, ಭಾರತವು ವಿಶ್ವ ದರ್ಜೆಯ ಶೈಕ್ಷಣಿಕ ಸಂಸ್ಥೆಯನ್ನು ಹೊಂದುವುದು ವಾಸ್ತವದಿಂದ ಬಹು ದೂರದ ಕನಸು ಎನ್ನುವುದು ಕಹಿ ಸತ್ಯ. ಇದು ಆದಷ್ಟು ಬೇಗ ನಮಗೆ ಅರಿವಾಗಬೇಕಿದೆ. ಇದರಿಂದ ಅಂಥ ಶಿಕ್ಷಣ ಸಂಸ್ಥೆಗಳನ್ನು ರೂಪಿಸುವ ಅಗತ್ಯವೇನು ಹಾಗೂ ಅದಕ್ಕಾಗಿ ತೆಗೆದುಕೊಳ್ಳಬೇಕಾದ ಪ್ರಾಯೋಗಿಕ ಹೆಜ್ಜೆಗಳೇನು ಎನ್ನುವ ಬಗ್ಗೆ ತಿಳಿದುಕೊಳ್ಳುವುದು ಸುಲಭವಾಗಲಿದೆ.\n*ಲೇಖಕರು ಮೂಲತಃ ಐಐಟಿ - ಮದ್ರಾಸ್ನ ವಿದ್ಯಾರ್ಥಿ; ವಿದ್ಯಾರ್ಥಿ ವಿನಿಮಯ ಯೋಜನೆಯಡಿ ಜರ್ಮನಿಯ ಆಚೆನ್ ವಿಶ್ವವಿದ್ಯಾಲಯದಿಂದ ಪದವಿಯನ್ನೂ, ಸ್ನಾತಕೋತ್ತರ ಪದವಿಯನ್ನೂ ಪಡೆದಿದ್ದಾರೆ. ಪ್ರಸ್ತುತ ಮ್ಯಾಕ್ಸ್ ಪ್ಲಾಂಕ್ ಇನ್ಸ್ಟಿಟ್ಯೂಟ್ನಲ್ಲಿ ಪಿಎಚ್ಡಿ ವಿದ್ಯಾರ್ಥಿ.
```


### Sangraha unverified — Marathi

- **S3 key:** `datasets/sangraha/unverified/mar/data-0.parquet`
- **Column:** `text`
- **Document id:** `85fbf4e9b5976499f9f5bf51d8044c8bdf0c28965eba02a86a9b323d08944e19` (column `doc_id`)
- **Character length:** 1,157

```
पुणे । शिरूर लोकसभा मतदार संघात येणाऱ्या पुणे- नगर रस्त्याचे काम गेल्या अनेक दिवसांपासून रखडले आहे. या मार्गावर होणारी वाहतूक कोंडी गेल्या अनेक वर्षांपासून डोकेदुखी ठरत आहे. यामुळे या रस्त्याचे काम कधी होणार हा प्रश्न विचारला जात होता.
या मार्गावर मोठ्या प्रमाणावर अपघात देखील झाले आहेत. यामध्ये अनेकांनी आपले जीव देखील गमावले आहेत. मात्र आता अमोल कोल्हेंच्या पुढाकाराने नितीन गडकरी यांनी पुणे-नगर-औरंगाबाद हा राष्ट्रीय महामार्ग क्र. ७५३ एफ म्हणून घोषित केला आहे.
आता 'भारतमाला परियोजना' अंतर्गत हा प्रकल्प राबविण्यात येणार आहे. केंद्रीय रस्ते परिवहन मंत्रालयाच्या सूचनेनुसार हा मार्ग ग्रीनफिल्ड द्रुतगती मार्ग म्हणून विकसित करण्यात येणार आहे. याबाबतचे पत्र केंद्रीय मंत्री नितीन गडकरी यांनी पाठवले आहे.
आता केंद्राच्या अर्थविषयक मंत्रिमंडळ समितीने मान्यता दिल्यानंतर हा प्रकल्प हाती घेण्यात येणार आहे. गेल्या अनेक वर्षांपासून या रोडचे काम करण्याची मागणी केली जात होती.
या मार्गावरील बाह्यवळण मार्ग तसेच चाकण, शिक्रापूर, नाशिक फाटा येथील कामांना प्राधान्य असेल. यामुळे शिरूर लोकसभा मतदारसंघातील वाहतूक कोंडीचा प्रश्न कायमचा मिटणार असल्याचे खासदार अमोल कोल्हे यांनी सांगितले. दिल्लीत अधिवेशन काळात आपण हा मुद्दा उपस्थित केला असल्याचे देखील त्यांनी सांगितले.
```


### Sangraha unverified — Gujarati

- **S3 key:** `datasets/sangraha/unverified/guj/data-0.parquet`
- **Column:** `text`
- **Document id:** `6f38f5d96f80dfa5305594c2cc5d56721e1e467560883a098c75be29441d1fbb` (column `doc_id`)
- **Character length:** 3,552

The first 700 characters, then the last 700. 2,152 characters were cut from the middle.

```
તમારા રસોડાના મંત્રીમંડળ માટે રંગ પસંદ કરવામાં મુશ્કેલી આવી રહી છે? તેમને ટુ-ટોન પેઇન્ટ જોબ કેમ ન આપો?
વ્હાઇટ સબવે ટાઇલ બેકસ્પ્લેશ ભવ્ય છે, તેઓ ક્લાસિક છે, અને ... તેઓ દરેક જગ્યાએ છે. અહીં સાત સ્ટાઇલિશ (અને સસ્તું) વિકલ્પો છે.
હજુ પણ મારા એપિફાઇટ હૃદય રહો.
સ્માર્ટ શોપિંગઃ શું IKEA સ્ટોવ ખરેખર સારી ડીલ છે?
તમે પહેલેથી જ IKEA પાસેથી બુકકેસ અને ઘેટાંના કાદવ જેવી વસ્તુઓ ખરીદી શકો છો, પરંતુ શું તમે જાણો છો કે તમે ત્યાં પણ રસોડાના ઉપકરણો ખરીદી શકો છો?
તે કેકને ફ્રોસ્ટ કરવા જેટલું સરળ છે.
લીંબુ મલમ ઘરની અંદર સંઘર્ષ કરી શકે છે, પરંતુ પૂરતા ધ્યાનથી તે ખીલે છે. તમારા ઇન્ડોર જડીબુટ્ટીના બગીચાને શરૂ કરવા માટે આ ડોઝ અને ડોન્ટ્સને અનુસરો.
20 શ્રેષ્ઠ પેશિયો અને આઉટડોર મેકઓવર ઓલ ટાઇમ, ચિત્રો સાથે તેને સાબિત
```


2,152 characters cut

```
 તમારા લnનને પોતાનું વ્યક્તિગત માર્ગ માને છે, તો તેનું પરિણામ બગડેલું લોન અને ખરાબ સ્વભાવ હોઈ શકે છે. અમને એવું વિચારવું ગમશે કે પાળેલા માલિકોને તમારા પશુઓને તમારા લnનથી દૂર રાખવા માટે કહેલી સારી નિશાની યુક્તિ કરશે પરંતુ તે હંમેશા એવું હોતું નથી.
જોના ગેઇન્સ દ્વારા મેગ્નોલિયા હોમના સાત પેઇન્ટ કલર અહીં છે જે 'ફિક્સર અપરઃ વેલકમ હોમ'ના એપિસોડમાં દર્શાવવામાં આવ્યા હતા.
વોલ ટ્રીમ એક મજબૂત દ્રશ્ય સંકેત છે, જે એક નજરમાં રૂમની સ્થાપત્ય શૈલીને વ્યક્ત કરે છે. પેનલ મોલ્ડિંગ અને ખુરશી રેલ પરંપરાગત ઘરો સાથે સૌથી નજીકથી સંકળાયેલી છે, પરંતુ ભૌમિતિક અને પુનરાવર્તિત આકારમાં લાકડાની ટ્રીમ સરળતાથી આધુનિક દેખાઈ શકે છે. પેટર્ન અને ટેક્સચર સાથે સપાટ સપાટીઓને પરિવર્તિત કરવાની સસ્તી રીત તરીકે આ વિચારોનો ઉપયોગ કરો.
```


### FineWeb 2 — Hindi

- **S3 key:** `datasets/fineweb2-indic/hin_Deva/train/000_00000.parquet`
- **Column:** `text`
- **Document id:** `<urn:uuid:4969b555-2e2b-4ca0-a99e-2c7f1f129e71>` (column `id`)
- **Character length:** 1,945

The first 700 characters, then the last 700. 545 characters were cut from the middle.

```
चीन में एक समय चोरों का बड़ा आतंक था. राज्य की राजधानी में ची युंग नामक एक व्यक्ति था जो किसी भी व्यक्ति का चेहरा देखकर यह बता देता था कि वह व्यक्ति चोर है या नहीं. सामनेवाले व्यक्ति के मुखमंडल के कुछ लक्षणों और उसके मन में चल रहे भावों को पढने में उसे महारत हासिल थी. उसका यह कौशल देखकर वहां के राजा ने उसे राज्य के नागरिकों के निरीक्षण में लगा दिया. ची युंग ने हजारों नागरिकों को देखा और उनमें से चोरों की पहचान कर ली. ची युंग ने चोरों को ढूंढ निकाला और राज्य में सर्वत्र खुशहाली छा गई.
राजा ने लाओ-त्ज़ु से ची युंग की बड़ी तारीफ की और कहा – “ची युंग ने अकेले ही राज्य को चोरों-डाकुओं से रिक्त कर दिया है. मेरे राज्य में अब हर तरफ शांति है. ची युंग के कारण मुझे न्याय-व्यवस्था पर कुछ भी खर्च नहीं क
```


545 characters cut

```
ा लाओ-त्ज़ु के पास गया और उससे बोला – “आपकी आशंका सत्य सिद्ध हो गई. ची युंग की हत्या हो गई है. अब मेरे राज्य की सुरक्षा खतरे में है.”
लाओ-त्ज़ु ने कहा – “एक पुरानी कहावत है, ‘अथाह समुद्र के तल में मछली पकड़ने वाले और गुप्त रहस्यों को व्यर्थ ही ढूँढने वाले अपने विनाश को निमंत्रण देते हैं’. यदि आप चोरों और डाकुओं से मुक्ति पाना चाहते हैं तो प्रशासन में सज्जन व्यक्तियों की नियुक्ति करें. उन्हें निर्देश दें कि वे अपने से ऊपर वालों को मार्गदर्शन दें और अपने से नीचे वालों को शिक्षित करें. जब लोग विधि और नियमों का पालन करने लगेंगे तो आपके राज्य में चोरों-डाकुओं के बनने का मार्ग स्वतः बंद हो जायेगा.”
राजा ने लाओ-त्ज़ु के बताये अनुसार प्रशासन में सुधार किये और धीरे-धीरे उसका राज्य आदर्श राज्य बन गया.
```


### FineWeb 2 — Bengali

- **S3 key:** `datasets/fineweb2-indic/ben_Beng/train/000_00000.parquet`
- **Column:** `text`
- **Document id:** `<urn:uuid:d84702b0-67f8-48f2-bf47-af9c8e90474e>` (column `id`)
- **Character length:** 18,827

The first 700 characters, then the last 700. 17,427 characters were cut from the middle.

```
প্রবাসী লেখকদের কলাম
একালের বাংলা সাহিত্যের সবচেয়ে জননন্দিত লেখক সদ্য প্রয়াত হুমায়ূন আহমেদের বেশিরভাগ লেখায় তাঁর প্রথম স্ত্রী গুলতেকিন এবং সন্তান নোভা-শীলা-বিপাশা-নুহাশদের প্রতি অদ্ভুত ভালবাসা দেখা গেছে । আবার দ্বিতীয় বিয়ের পর তাঁর সাহিত্যে অভিনেত্রী শাওন ও তার দুই ছেলে নিষাদ-নিনিত`র উপস্থিতি ছিল প্রবল।
আর এসময় প্রথম পক্ষের স্ত্রী-সন্তানরা ক্রমশ তাঁর জীবন ও সাহিত্য থেকে আড়াল হয়ে যায় । তবে ক্যান্সারের চিকিৎসার জন্য যুক্তরাষ্ট্রে অবস্থানকালীন তার লেখা ‘তিন ডব্লিউ’’তে উঠে আসে কন্যা নোভা, শিলা ও বিপাশা আহমেদের কথা।
আর এ লেখাতে যেমন ছিল কন্যাদের প্রতি তার অন্যরকম ভাললাগার কথা, তেমনি ছিল তাদের উপেক্ষা করারও কিছু কথা। যা তুলে ধরা হলো:
আমার এখন চার নাতি-নাতনি। আমি যেখানে বাস করি, তা তাদের 
```


17,427 characters cut

```
বাঁচবে। তিনি প্রথমটাই ধরে নিয়েছিলেন। দু বছর। সেই কারণেই অপেক্ষা চলছিল এবং এই সময়ের ভেতরে আরো কিছু কাজ করে যেতে চেয়েছিলেন।
৩০ জুন, রোববার। বেলা ২টা হবে। ম্যানহাটন ডাউন টাউন। ১৪ নং স্ট্রিট এবং ইউনিয়ন স্কয়ারের মোড়। আমার গাড়িতে করে আমি, পূরবী বসু, শাওন এবং মাজহার ওখানে পৌঁছি। ‘বেস্ট বাই’ দোকান থেকে একটা ভয়েস-রেকর্ডার কেনা হয়। হুমায়ূন আহমেদের শেষ কথাগুলো রেকর্ড করার জন্য। মনে হয় তা আর হয়ে ওঠেনি। তখন মাজহার আর শাওন স্বপ্নের ঘোরে বাস করছিলেন। আমি যা দেখেছি-বুঝেছি তার অবস্থা দেখে মনে হয়েছিল তিনি ২৮-২৯ জুন থেকে লাইফ সাপোর্টে চলে যান। যদি সেই সময়ে তিনি লাইফ সাপোর্টে না যেতেন, তাহলে তার শেষ ইচ্ছাগুলো অনায়াসে রেকর্ড করা যেত। আজ তার দাফন নিয়ে এত জটিলতা দেখা দিত না।
|< পূববর্তী||পরবর্তী >|
```


### FineWeb 2 — Tamil

- **S3 key:** `datasets/fineweb2-indic/tam_Taml/train/000_00000.parquet`
- **Column:** `text`
- **Document id:** `<urn:uuid:1d15e0c4-2e83-4056-a0e5-9c189c6e0559>` (column `id`)
- **Character length:** 907

```
ராமநாதபுரம் ஜில்லா போர்டு தலைவர் W.P.A. சவுந்தரபாண்டியன் அவர்கள் மோட்டார் கம்பெனி முதலாளிகளுக்குப் பின்வருமாறு ஒரு சுற்றுக் கடிதம் அனுப்பியிருக்கிறார்கள். அது வருமாறு:
இந்த ஜில்லாவிலுள்ள சில மோட்டார் கம்பெனி முதலாளிகள் ஆதி திராவிடர்களை தமது பஸ்களில் ஏற்றிக் கொண்டு போவதில்லையென்றும் டிக்கெட்டில், ஆதிதிராவிடர்களுக்கு டிக்கட்டு கொடுக்கப்பட மாட்டாது என்று நிபந்தனை ஏற்படுத்தியிருப்பதாகவும் அறிகின்றோம்.
இவ் வழக்கம் பிரயாணிகளுக்கு இடைஞ்சல் உண்டு பண்ணத் தக்கதாகவும், மிக அக்கிரம மானதாகவும் இருக்கிறது.
ஆகவே மோட்டார் கம்பெனி முதலாளிகள் ஏதேனும் ஒரு சமூகத்தாரை பஸ்சில் ஏற்றிச் செல்ல மறுக்கவோ, டிக்கெட்டுகளில் மறுப்பு விதிகள் அச்சிடவோ செய்தால் அவர்களுடைய லைசென்சு முன்னறிக்கை கொடாமலே ரத்து செய்யப் படுமென இதனால் எச்சரிக்கை செய்கிறோம். இந்தச் சுற்றுக் கடிதம் கிடைத்து ஒரு வாரத்திற்குள் அந்தத் தடை விதி நீக்கப் பட்டதா அல்லவா என்று சாம்பிள் டிக்கெட்டுடன் ரிப்போர்ட் செய்து கொள்ள வேண்டும்.-
குடிஅரசு 4-.9.-1930 பக். 13)
```


### FineWeb 2 — Telugu

- **S3 key:** `datasets/fineweb2-indic/tel_Telu/train/000_00000.parquet`
- **Column:** `text`
- **Document id:** `<urn:uuid:894cbbd7-1cc2-4753-9f9c-2d48d5a2d2f4>` (column `id`)
- **Character length:** 596

```
టాలీవుడ్ లో కళ్యాణ్ హీరోగా వచ్చిన కత్తి సినిమాలో , ఆ తరువాత మంచు మనోజ్ హీరోగా వచ్చిన మిస్టర్ నూకయ్య చిత్రాలలో నటించిన హాట్ భామ సనాఖాన్ గత కొన్నాళ్ళ నుండి వెండితెర పై కనిపించడం లేదు. తాజాగా ఈమె బిగ్ బాస్ - 6షోలో ఛాన్స్ కొట్టేసి మళ్ళీ ప్రేక్షకుల ముందుకు వచ్చింది. సనా ఖాన్ కి ఇదే మంచి అవకాశం అనుకుంటే అంత కంటే ఎక్కువ మంచి అవకాశం కొట్టేసింది. అదేంటంటే... బాలీవుడ్ కండల వీరుడు సల్మాన్ ఖాన్ సనాఖాన్ బిగ్ బాస్ షోలో చేసిన డాన్స్ కి ఫిధా అయిపోయి, ఆమెకు తన సినిమాలో అవకాశం కల్పిస్తానని హామి ఇచ్చాడట. ఒకవేళ సల్లూభాయ్ సనాఖాన్ కి తన సినిమాలో ఆఫర్ ఇస్తే...ఈమె దశ తిరిగినట్లే అని బాలీవుడ్ జనాలు అనుకుంటున్నారు.
```


### FineWeb 2 — Kannada

- **S3 key:** `datasets/fineweb2-indic/kan_Knda/train/000_00000.parquet`
- **Column:** `text`
- **Document id:** `<urn:uuid:00863128-cd81-4b8b-80a8-285a070da163>` (column `id`)
- **Character length:** 5,274

The first 700 characters, then the last 700. 3,874 characters were cut from the middle.

```
ಜಾಗತೀಕರಣದ ಅಬ್ಬರ ಮತ್ತು ಸ್ಥಳೀಯ ಮಾರುಕಟ್ಟೆಯಲ್ಲಿನ ವಿದೇಶಿ ಸ್ಪರ್ಧೆಗಳನ್ನು ಯಾವುದೇ ಭಾವಾವೇಶಕ್ಕೆ ಒಳಗಾಗದೆ ಭಾರತೀಯರು ಸಮರ್ಥವಾಗಿ ಉದ್ದಿಮೆಗಳನ್ನು ಮುನ್ನಡೆಸುತ್ತಿದ್ದಾರೆ.
ಕಳೆದ ಕೆಲವು ತಿಂಗಳುಗಳಿಂದ ಎಲ್ಲೆಲ್ಲೂ ಉದ್ಯಮಿ ವಿಜಯ್ ಮಲ್ಯರದ್ದೇ ಸುದ್ದಿ. ಉದ್ಯಮದಲ್ಲಿ ಅವರು ಎದುರಿಸುತ್ತಿರುವ ಸಂಕಷ್ಟ, ಇನ್ನೇನು ಅವರ ಕಥೆ ಮುಗಿದೇ ಹೋಯ್ತು ಎಂದು ಸಂತಾಪ ಸೂಚಿಸಿ ಅನೇಕರು ಪುಟಗಟ್ಟಳೆ ಬರೆದುಬಿಟ್ಟರು. ಅವರ ಪ್ರಮುಖ ಉದ್ದಿಮೆ ಯುನೈಟೆಡ್ ಸ್ಪಿರಿಟ್ಸ್ ನ ಬಹುತೇಕ ಷೇರುಗಳನ್ನು ವಿದೇಶಿ ಕಂಪನಿ ಡಿಯಾಗೊಗೆ ಮಾರಿದ್ದು, ತಮ್ಮ ವಿಮಾನಯಾನ ಸಂಸ್ಥೆ ಕಿಂಗ್ ಫಿಶರ್ ಏರ್ಲೈನ್ಸ್ ನಲ್ಲಿ ಬಂಡವಾಳ ಹೂಡುವಂತೆ ವಿದೇಶಿ ಕಂಪನಿಗಳ ಮನವೊಲಿಕೆಗೆ ಮಲ್ಯ ನಡೆಸಿದ ಕಸರತ್ತು ಬರೆಯುವವರಿಗೆ ಇನ್ನಷ್ಟು ಸರಕು ಒದಗಿಸಿತು. ಕೆಲವರಂತೂ ಮೂರು ದಶಕಗಳ ಕಾಲ ಮಲ್ಯ ಕಷ್ಟಪಟ್ಟು, ತುಂಬಾ ಎಚ್ಚರಿಕೆಯಿಂದ ಕಟ್ಟಿದ ಸಾಮ್ರಾಜ್ಯ ಪತನಗೊಂಡಿತು ಎಂದು ಬೇಸರದಿಂದ ಲೊಚಗುಟ್ಟಿದರು. ಆದರೆ ಇದು ನಿಜವೇ? ಮಲ
```


3,874 characters cut

```
ದಾರೆ. ನನ್ನ ಮಾತು ಮನದಟ್ಟಾಗಬೇಕಾದರೆ ಟಾಟಾ ಸಮೂಹವು ಕೋರಸ್ ಸ್ಟೀಲ್ ಮತ್ತು ಜಾಗ್ವರ್/ ಲ್ಯಾಂಡ್ ರೋವರ್ಗಳ ಮೇಲೆ ಹಿಡಿತ ಸಾಧಿಸಿದ್ದು, ಕುಮಾರ ಮಂಗಲಂ ಬಿರ್ಲಾ ಹಲವಾರು ವಿದೇಶಿ ಕಂಪನಿಗಳಲ್ಲಿ ಬಂಡವಾಳ ಹೂಡಿದ್ದನ್ನು ನೆನಪಿಸಿಕೊಳ್ಳಿ.
ಎಲ್ಲಿ ವಿದೇಶಿ ಕಂಪನಿಗಳಿಗೆ ಸೂಕ್ತ ಪ್ರತಿಸ್ಪರ್ಧೆ ನೀಡಲಾಗುತ್ತಿಲ್ಲ, ಅವರಿಗೆ ಪೈಪೋಟಿ ನೀಡುವ ಕೌಶಲ ತಮಗಿಲ್ಲ ಎಂದು ಮನದಟ್ಟಾದರೆ ಭಾರತೀಯ ಉದ್ಯಮಿಗಳು ಯಾವುದೇ ಹಿಂಜರಿಕೆಯಿಲ್ಲದೆ, ಪಕ್ಕಾ ವೃತ್ತಿಪರರಂತೆ ಕಂಪನಿಗಳನ್ನು ಮಾರಿ, ಹೊಸ ಹೊಸ ಅವಕಾಶಗಳನ್ನು ಹುಡುಕಿಕೊಂಡು ಹೊಸ ಉದ್ದಿಮೆಗಳತ್ತ ಹೆಜ್ಜೆ ಹಾಕುತ್ತಾರೆ. ಅದು ಹಣಕಾಸಿನ ಬಲವೇ ಇರಬಹುದು, ತಂತ್ರಜ್ಞಾನದ ಲಭ್ಯತೆ ಅಥವಾ ನಿರ್ವಹಣಾ ಸಾಮರ್ಥ್ಯ ವಿಷಯ ಯಾವುದೇ ಇರಲಿ ಸ್ಥಳೀಯ ಮಾಲೀಕರು ಕೈಕಟ್ಟಿ ಕುಳಿತು ತಾವು ಕಟ್ಟಿ ಬೆಳೆಸಿದ ಸಾಮ್ರಾಜ್ಯಗಳ ಪತನವನ್ನು ನೋಡುತ್ತಾ ಸುಮ್ಮನಿರುವುದಿಲ್ಲ. ಹೊಸ ಉದ್ಯಮಗಳಲ್ಲಿ ಹೂಡಿ ಮತ್ತೆ ಪುಟಿದೇಳುತ್ತಾರೆ. ಬೂದಿಯಿಂದೆದ್ದು ಬಂದ ಫೀನಿಕ್ಸ್ನಂತೆ.
```


### FineWeb 2 — Marathi

- **S3 key:** `datasets/fineweb2-indic/mar_Deva/train/000_00000.parquet`
- **Column:** `text`
- **Document id:** `<urn:uuid:b4a50889-e321-4fb8-b165-0d0ffb240bfe>` (column `id`)
- **Character length:** 785

```
www.24taas.com, भोपाळ
मध्य प्रदेशात लाईव्ह एन्टाऊंटर नाट्य घडलं. त्याचं असं झालं की, दरोडेखोरांनी लूट करताना तीन लाख पळविले. मात्र, पोलिसांना माहिती मिळताच त्यांनी घेराव घातला. पोलिसांना शरण येण्याऐवजी लुटारूंनी गोळीबार केला आणि चकमक झाली.
मध्यप्रदेशातल्या एका गावात तीन दरोडेखोरांनी एका ठिकाणी तीन लाख रुपयांची लूट केली होती. पोलिसांना याची माहिती मिळताच दरोडेखोरांनी पैसे घेऊन तिथून पळ काढला. पोलिसांनी त्यांचा पाठलाग केला, दरोडेखोर एका घरात लपले होते. त्या ठिकाणी पोलिसांनी त्यांना पकडण्याचा प्रयत्न केला. मात्र दरोडेखोरांनी पोलिसांवर गावठी कट्ट्यातून गोळीबार केला. त्याला प्रत्युत्त म्हणून पोलिसांनीही गोळीबार केला.
पोलीस आणि दरोडेखोरांमध्ये तब्बल पाच तास एन्काऊंटर सुरू होतं. त्यामध्ये एक दरोडेखोर ठार झाला. तर दोन पोलीसही जखमी झाले.
First Published: Saturday, May 26, 2012, 19:47
```


### FineWeb 2 — Gujarati

- **S3 key:** `datasets/fineweb2-indic/guj_Gujr/train/000_00000.parquet`
- **Column:** `text`
- **Document id:** `<urn:uuid:8f8d748c-b316-4f56-aecb-885522659490>` (column `id`)
- **Character length:** 2,177

The first 700 characters, then the last 700. 777 characters were cut from the middle.

```
સાયબરજગતમાં ‘દો કિસ્મ કે લોગ હોતે હૈં - એક જો ટેક્નોલોજી કા સહી ઉપયોગ કરતે હૈં, ઔર દૂસરે જો...' આ ‘દૂસરે' ટાઇપના લોકોમાં વાયરસ, સ્પાયવેર્સ, એડવેર્સ, ટ્રોજન, કી-લોગર્સ વગેરે વગેરેનો ફેલાવો કરનારા લોકોનો સમાવેશ થાય છે.
આ બધાં નામ જેમને થોડાં અજાણ્યાં લાગ્યાં હોય એમના માટે જરા ક્વિક રેફરન્સ...
વાયરસ એટલે આપણી જાણ બહાર કમ્પ્યુટરમાં ઘૂસી જતો નાનો પ્રોગ્રામ. જે મેડિકલ વાયરસની જેમ જ, કમ્પ્યુટરમાં હાહાકાર મચાવી શકે, સિસ્ટમ ક્રેશ કરી શકે, બધો ડેટા ભૂંસી શકે.
સ્પાયવેર જરા જુદા, એ તમારા કમ્પ્યુટરમાં ઘૂસ્યા પછી, તમારી બાતમી - પાસવર્ડ, ક્રેડિટ કાર્ડના નંબર વગેરે - પોતાના મૂળ માલિક, સ્પાયવેર તૈયાર કરનાર વ્યક્તિ કે વેબસાઇટને પહોંચાડે છે.
એડવેર, તેના નામ પ્રમાણે કમ્પ્યુટરમાં ઘૂસીને જાત-ભાતની એડ્સ પોપ-અપ કરે
```


777 characters cut

```
ય ત્યારે `યોર ટ્રુ લવ' કે `વીથ ટેન્ડર લવ' જેવા સબ્જેક્ટ સાથેના ઇ-મેઇલ્સ ખોલવાનું કોઈને પણ મન થાય અને પછી તો...!
અલબત્ત, સાયબરજગતમાં ‘જે પોષતું તે મારતું' કરતાં જુદો સીન પણ છે. અવાસ્ટ, એવીજી વગેરે નામ સાથે એન્ટીવાયરસ કે એન્ટીસ્પાયવેર લખીને સર્ચ કરશો એટલે, હોમ કે નોન-કમર્શિયલ યૂઝ માટે ફ્રી એન્ટીવાયરસ પ્રોગ્રામ આપતી સાઇટસ પર પહોંચશો. ગૂગલ ‘ગૂગલ પેક' નામે ઉપયોગી સોફ્ટવેર ફ્રી ડાઉનલોડ કરવા આપે છે એમાં પણ એન્ટીવાયરસ પ્રોગ્રામ છે.
આ બધા પ્રોગ્રામ એકવાર ડાઉનલોડ કર્યા પછી, તમે જ્યારે પણ નેટસર્ફિંગ કરો ત્યારે આપોઆપ નવા શોધાયેલા વાયરસની ડેફિનેશન ડાઉનલોડ કરીને કોમ્પ્યુટરને પ્રોટેક્ટ કરતા રહે છે. નિયમિત સ્કૅન કરવાની જવાબદારી તમારી, પણ પાયરેટેડ પ્રોગ્રામ કે કમ્પ્યૂટર વેન્ડરને ભરોસે રહેવાની જરૂર રહેતી નથી.
```


### IndicCorp v2 — Hindi

- **S3 key:** `datasets/indiccorp-v2/hin_Deva/hi-1.txt`
- **Column:** none. IndicCorp is one document per line. This is line 1, the first non-empty line.
- **Document id:** none. This file has no id column.
- **Character length:** 45

```
लोगों को बिलों संबंधी सुविधा देना ही उनका काम
```


### IndicCorp v2 — Bengali

- **S3 key:** `datasets/indiccorp-v2/ben_Beng/bn.txt`
- **Column:** none. IndicCorp is one document per line. This is line 1, the first non-empty line.
- **Document id:** none. This file has no id column.
- **Character length:** 410

```
নয়াদিল্লি: আজ ভ্যালেন্টাইনস ডে। এমন একটি দিনে প্রিয় মানুষকে হৃদয় উজাড় করা ভালোবাসার বার্তা দিতে পৌঁছে দিতে উন্মুখ অনেকেই। এমন একটি দিনে ভারতীয় দলের প্রাক্তন ক্রিকেটার সচিন তেন্ডুলকর জানালেন তাঁর প্রথম ভালোবাসার কথা। একটি ভিডিও পোস্ট করেছেন ভারতীয় দলের প্রাক্তন ব্যাটিং স্তম্ভ। ভিডিওতে আন্তর্জাতিক ক্রিকেট ১০০ শতরানের মালিককে নেটে অনুশীলন করতে দেখা যাচ্ছে। ওই ভিডিও শেয়ার করে সচিন লিখেছেন, আমার প্রথম ভালোবাসা।
```


### IndicCorp v2 — Tamil

- **S3 key:** `datasets/indiccorp-v2/tam_Taml/ta.txt`
- **Column:** none. IndicCorp is one document per line. This is line 1, the first non-empty line.
- **Document id:** none. This file has no id column.
- **Character length:** 314

```
இதுகுறித்து அமெரிக்கன் ஏர்லைன்ஸ், ஒழுங்குமுறை மற்றும் சர்வதேச விவகாரங்களின் துணைத் தலைவர் மோலி வில்கின்சன் கூறுகையில், ” உலக நாடுகளுக்கு இடையிலான பயணத்தை எளிதாக்குவதும் மூலம், புதிய வழித்தடங்களும், விருப்பங்களும் விரைவில் செயல்பாட்டுக்கு வரும். இது, சர்வதேச பயணத்தை அதிகரிக்கும் என எதிர்பார்க்கப்படுகிறது” என்றார்.
```


### IndicCorp v2 — Telugu

- **S3 key:** `datasets/indiccorp-v2/tel_Telu/te.txt`
- **Column:** none. IndicCorp is one document per line. This is line 1, the first non-empty line.
- **Document id:** none. This file has no id column.
- **Character length:** 201

```
అమెరికా అధ్యక్షుడు డొనాల్డ్ ట్రంప్ కు రాష్ట్రపతి  భవన్ వద్ద ఘనస్వాగతం లభించింది. ఆయనకు రాష్ట్రపతి రామ్ నాథ్ కోవింద్ దంపతులు, ప్రధాని మోదీ సాదరంగా ఆహ్వానం పలకడంతో పాటు సైనికులు గౌరవ వందనాన్ని అందించారు.
```


### IndicCorp v2 — Kannada

- **S3 key:** `datasets/indiccorp-v2/kan_Knda/kn.txt`
- **Column:** none. IndicCorp is one document per line. This is line 1, the first non-empty line.
- **Document id:** none. This file has no id column.
- **Character length:** 16

```
ಸ್ವ ಉಪಕರಣ ಮೂಲಕ -
```


### IndicCorp v2 — Marathi

- **S3 key:** `datasets/indiccorp-v2/mar_Deva/mr.txt`
- **Column:** none. IndicCorp is one document per line. This is line 1, the first non-empty line.
- **Document id:** none. This file has no id column.
- **Character length:** 527

```
ऊती संवर्धन तंत्राचे अनेक उपयोग आहेत. या तंत्राचा उपयोग विशेषकरून जीवशास्त्र व वैद्यकशास्त्रात होतो. वयोवृद्धी, पोषण, लसनिर्मिती, जन्मजात रोगांचे निदान, इंद्रियांचे रोपण, कर्करोग संशोधन व गर्भपोषण या क्षेत्रांत ऊती संवर्धन तंत्र प्रामुख्याने वापरले जाते. पेशींच्या चयापचयावर एखाद्या घटकाचा परिणाम पाहणे, सामान्य किंवा कर्करोगाच्या पेशींवर औषधांचा होणारा परिणाम पाहणे, प्रयोगशाळेत त्वचा तयार करणे इ. बाबी ऊती संवर्धनामुळे शक्य झाल्या आहेत. भाजलेल्या रुग्णाच्या त्वचारोपणासाठी ऊती संवर्धनाद्वारे निर्माण केलेली त्वचा वापरली जाते.
```


### IndicCorp v2 — Gujarati

- **S3 key:** `datasets/indiccorp-v2/guj_Gujr/gu.txt`
- **Column:** none. IndicCorp is one document per line. This is line 1, the first non-empty line.
- **Document id:** none. This file has no id column.
- **Character length:** 54

```
આ વીડિયો જુઓ: ઊંઝા માર્કેટયાર્ડ આજથી 25 જુલાઈ સુધી બંધ
```


### BhashaWiki — Hindi

- **S3 key:** `datasets/bhashawiki/hin_Deva/train-001-of-11.parquet`
- **Column:** `text`
- **Document id:** `63047548` (column `id`)
- **Character length:** 2,082

The first 700 characters, then the last 700. 682 characters were cut from the middle.

```
पी. एस. नटराज पिल्लई (मार्च 1891-1966) एक भारतीय राजनेता, स्वतंत्रता सेनानी और 1962 में हुए तीसरे लोकसभा चुनाव के दौरान संसद सदस्य थे। उन्होंने 1948 में दिल्ली में त्रावणकोर सरकार के सलाहकार और 1954 से 1955 तक त्रावणकोर-कोच्चि राज्य के वित्त मंत्री के रूप में कार्य किया। जीवन और पृष्ठभूमि पी. एस. नटराज का जन्म मार्च 1891 में केरल के अलप्पुड़ा जिले में हुआ था। उन्हें मूल रूप से 1962 में स्वतंत्र रूप से संसद सदस्य के रूप में चुना गया था; बाद में, उन्होंने कांग्रेस, भारतीय समाजवादी पार्टी और प्रजा समाजवादी पार्टी के साथ अपने राजनीतिक संघों की स्थापना की। भारत की स्वतंत्रता से पहले, वे 1946 में त्रावणकोर संविधान सुधार समिति के सदस्य थे। अपने कार्यकाल के दौरान, वे 1952 से 1953 तक त्रावणकोर मणिगम 
```


682 characters cut

```
नटराज एक भारतीय विद्वान मनोमनियम पी. सुंदरम पिल्लई के पुत्र थे, जिन्हें पेशेवर रूप से प्रोफेसर मनोमनियम सुंदरम पिल्लई के नाम से जाना जाता था, जो केरल में स्थित एक कॉलेज में शिक्षक थे। विवाद 2017 में केरल के मुख्यमंत्री पिनाराई विजयन ने पी. एस. नटराज पिल्लई के बारे में आपत्तिजनक टिप्पणी करने का दावा किया था। मंत्री ने बाद में इन टिप्पणियों को स्वीकार करते हुए कहा कि उनका उद्देश्य कभी भी किसी विशेष व्यक्ति को नीचा दिखाना नहीं था, बल्कि केवल कुछ पिल्लई परिवारों को नीचा दिखाना था। विजयन ने विवादों को स्पष्ट करते हुए कहा कि उन्हें नटराज का नाम भी याद नहीं है। विपक्षी दल भारतीय राष्ट्रीय कांग्रेस ने केरल के मुख्यमंत्री की टिप्पणी को लेकर उनके इस्तीफे की मांग की, जिससे वे व्यापक विवाद में पड़ गए। ।
```


### BhashaWiki — Bengali

- **S3 key:** `datasets/bhashawiki/ben_Beng/train-001-of-11.parquet`
- **Column:** `text`
- **Document id:** `63047548` (column `id`)
- **Character length:** 2,057

The first 700 characters, then the last 700. 657 characters were cut from the middle.

```
পি. এস. নটরাজ পিল্লাই (মার্চ 1891-1966) একজন ভারতীয় রাজনীতিবিদ, স্বাধীনতা সংগ্রামী এবং 1962 সালে অনুষ্ঠিত তৃতীয় লোকসভা নির্বাচনের সময় সংসদ সদস্য ছিলেন। তিনি 1948 সালে দিল্লিতে ত্রিবাঙ্কুর সরকারের উপদেষ্টা এবং 1954 থেকে 1955 সাল পর্যন্ত ত্রিবাঙ্কুর-কোচিন রাজ্যের অর্থমন্ত্রী হিসেবে দায়িত্ব পালন করেন। জীবন ও পটভূমি পি. এস. নটরাজ 1891 সালের মার্চ মাসে কেরালার আলাপ্পুঝা জেলায় জন্মগ্রহণ করেন। তিনি মূলত 1962 সালে স্বাধীনভাবে সংসদ সদস্য নির্বাচিত হন; পরে, তিনি কংগ্রেস, ভারতীয় সমাজতান্ত্রিক দল এবং প্রজা সমাজতান্ত্রিক দলের সাথে তাঁর রাজনৈতিক সম্পর্ক স্থাপন করেন। ভারতের স্বাধীনতার আগে, তিনি 1946 সালে ট্রাভাঙ্কোর সংবিধান সংস্কার কমিটির সদস্য ছিলেন। কর্মজীবনে তিনি 1952 থেকে 1953 সাল পর্যন্ত ট্রাভাঙ
```


657 characters cut

```
ন এবং তাঁর সাত কন্যা ও তিন পুত্র ছিল। নটরাজ ছিলেন একজন ভারতীয় পণ্ডিত মনোমনিয়াম পি সুন্দরম পিল্লাইয়ের পুত্র, যিনি পেশাগতভাবে অধ্যাপক মনোমনিয়াম সুন্দরম পিল্লাই নামে পরিচিত, যিনি কেরালায় অবস্থিত একটি কলেজের শিক্ষক ছিলেন। বিতর্ক 2017 সালে, কেরালার মুখ্যমন্ত্রী পিনারাই বিজয়ন পি. এস. নটরাজ পিল্লাই সম্পর্কে আপত্তিকর মন্তব্য করার দাবি করেছিলেন। মন্ত্রী পরে এই মন্তব্য স্বীকার করে উল্লেখ করেন যে তিনি কখনই কোনও নির্দিষ্ট ব্যক্তিকে অবজ্ঞা করতে চাননি, কেবল কয়েকটি পিল্লাই পরিবারকে অবজ্ঞা করতে চেয়েছিলেন। বিজয়ন এই বলে বিতর্কগুলি স্পষ্ট করে দিয়েছিলেন যে তিনি নটরাজের নামও মনে রাখেননি। বিরোধী দল ভারতীয় জাতীয় কংগ্রেস কেরালার মুখ্যমন্ত্রীর পদত্যাগের দাবি জানিয়েছিল, যা তাঁকে ব্যাপক বিতর্কে ফেলেছিল। ।
```


### BhashaWiki — Tamil

- **S3 key:** `datasets/bhashawiki/tam_Taml/train-001-of-11.parquet`
- **Column:** `text`
- **Document id:** `63047548` (column `id`)
- **Character length:** 2,334

The first 700 characters, then the last 700. 934 characters were cut from the middle.

```
பி. எஸ். நடராஜ பிள்ளை (மார்ச் 1891,1966) ஒரு இந்திய அரசியல்வாதி, சுதந்திர போராட்ட வீரர் மற்றும் 1962 இல் நடைபெற்ற 3 வது மக்களவைத் தேர்தலின் போது நாடாளுமன்ற உறுப்பினர் ஆவார். 1948இல் தில்லியில் திருவிதாங்கூர் அரசின் ஆலோசகராகவும், 1954 முதல் 1955 வரை திருவிதாங்கூர்-கொச்சி மாநிலத்தின் நிதியமைச்சராகவும் பணியாற்றினார். வாழ்க்கை மற்றும் பின்னணி பி. எஸ். நடராஜர் மார்ச் 1891 இல் கேரளாவின் ஆலப்புழா மாவட்டத்தில் பிறந்தார். அவர் முதலில் 1962 இல் சுயாதீனமாக நாடாளுமன்ற உறுப்பினராக தேர்ந்தெடுக்கப்பட்டார்; பின்னர், அவர் காங்கிரஸ், இந்திய சோசலிஸ்ட் கட்சி மற்றும் பிரஜா சோசலிஸ்ட் கட்சியுடன் தனது அரசியல் தொடர்புகளை நிறுவினார். இந்திய சுதந்திரத்திற்கு முன்பு, அவர் 1946 இல் திருவிதாங்கூர் அரசியலமைப்பு சீர்திருத்
```


934 characters cut

```
க இருந்த பேராசிரியர் மனோன்மணியம் சுந்தரம் பிள்ளை என்று தொழில் ரீதியாக அறியப்பட்ட இந்திய அறிஞர் மனோன்மணியம் பி. சுந்தரம் பிள்ளையின் மகன் நடராஜர் ஆவார். சர்ச்சைகள் 2017 ஆம் ஆண்டில், கேரள முதலமைச்சர் பினராயி விஜயன் பி. எஸ். நடராஜ பிள்ளை குறித்து ஆட்சேபனைக்குரிய கருத்துக்களை தெரிவித்ததாகக் கூறினார். அமைச்சர் பின்னர் ஒரு குறிப்பிட்ட நபரை இழிவுபடுத்துவதை ஒருபோதும் நோக்கமாகக் கொண்டிருக்கவில்லை, ஆனால் சில பிள்ளை குடும்பங்களை மட்டுமே இழிவுபடுத்துவதாகக் குறிப்பிட்டார். நடராஜரின் பெயர் கூட தனக்கு நினைவில் இல்லை என்று கூறி விஜயன் சர்ச்சைகளை தெளிவுபடுத்தினார். எதிர்க்கட்சியான இந்திய தேசிய காங்கிரஸ், கேரள முதல்வரின் கருத்துக்களுக்காக அவரை ராஜினாமா செய்யக் கோரியது, இது அவரை பரந்த சர்ச்சையில் ஆழ்த்தியது. ..
```


### BhashaWiki — Telugu

absent

No folder for Telugu under `datasets/bhashawiki/`.

### BhashaWiki — Kannada

- **S3 key:** `datasets/bhashawiki/kan_Knda/train-001-of-11.parquet`
- **Column:** `text`
- **Document id:** `63047548` (column `id`)
- **Character length:** 2,153

The first 700 characters, then the last 700. 753 characters were cut from the middle.

```
ಪಿ. ಎಸ್. ನಟರಾಜ ಪಿಳ್ಳೈ (ಮಾರ್ಚ್ 1891-1966) ಒಬ್ಬ ಭಾರತೀಯ ರಾಜಕಾರಣಿ, ಸ್ವಾತಂತ್ರ್ಯ ಹೋರಾಟಗಾರ ಮತ್ತು 1962ರಲ್ಲಿ ನಡೆದ 3ನೇ ಲೋಕಸಭಾ ಚುನಾವಣೆಯಲ್ಲಿ ಸಂಸತ್ ಸದಸ್ಯರಾಗಿದ್ದರು. ಅವರು 1948ರಲ್ಲಿ ದೆಹಲಿಯಲ್ಲಿ ತಿರುವಾಂಕೂರ್ ಸರ್ಕಾರದ ಸಲಹೆಗಾರರಾಗಿ ಮತ್ತು 1954ರಿಂದ 1955ರವರೆಗೆ ತಿರುವಾಂಕೂರ್-ಕೊಚ್ಚಿನ್ ರಾಜ್ಯದ ಹಣಕಾಸು ಸಚಿವರಾಗಿ ಸೇವೆ ಸಲ್ಲಿಸಿದರು. ಜೀವನ ಮತ್ತು ಹಿನ್ನೆಲೆ ಪಿ. ಎಸ್. ನಟರಾಜರು 1891ರ ಮಾರ್ಚ್ನಲ್ಲಿ ಕೇರಳದ ಅಲಪ್ಪುಳ ಜಿಲ್ಲೆಯಲ್ಲಿ ಜನಿಸಿದರು. ಅವರು ಮೂಲತಃ 1962 ರಲ್ಲಿ ಸ್ವತಂತ್ರವಾಗಿ ಸಂಸತ್ ಸದಸ್ಯರಾಗಿ ಆಯ್ಕೆಯಾದರು; ನಂತರ, ಅವರು ಕಾಂಗ್ರೆಸ್, ಭಾರತೀಯ ಸಮಾಜವಾದಿ ಪಕ್ಷ ಮತ್ತು ಪ್ರಜಾ ಸಮಾಜವಾದಿ ಪಕ್ಷದೊಂದಿಗೆ ತಮ್ಮ ರಾಜಕೀಯ ಸಂಬಂಧಗಳನ್ನು ಸ್ಥಾಪಿಸಿದರು. ಭಾರತದ ಸ್ವಾತಂತ್ರ್ಯದ ಮೊದಲು, ಅವರು 1946ರಲ್ಲಿ ತಿರುವಾಂಕೂರು ಸಂವಿಧಾನ ಸುಧಾರಣಾ ಸಮಿತಿಯ ಸದಸ್ಯರಾಗಿದ್ದರು. ತಮ್ಮ ವೃತ್ತಿಜೀವನದ ಅವಧಿಯಲ್ಲಿ, ಅವರು 1952ರಿಂದ 195
```


753 characters cut

```
ಂ ಪಿಳ್ಳೈ ಎಂದು ಕರೆಯಲ್ಪಡುವ ಭಾರತೀಯ ವಿದ್ವಾಂಸ ಮನೋನ್ಮಣಿಯಂ ಪಿ. ಸುಂದರಂ ಪಿಳ್ಳೈ ಅವರ ಪುತ್ರರಾಗಿದ್ದರು, ಅವರು ಕೇರಳದಲ್ಲಿರುವ ಕಾಲೇಜಿನೊಂದರಲ್ಲಿ ಶಿಕ್ಷಕರಾಗಿದ್ದರು. ವಿವಾದಗಳು 2017ರಲ್ಲಿ, ಕೇರಳದ ಮುಖ್ಯಮಂತ್ರಿ ಪಿಣರಾಯಿ ವಿಜಯನ್ ಅವರು ಪಿ. ಎಸ್. ನಟರಾಜ ಪಿಳ್ಳೈ ಬಗ್ಗೆ ಆಕ್ಷೇಪಾರ್ಹ ಹೇಳಿಕೆಗಳನ್ನು ನೀಡಿದ್ದಾರೆ ಎಂದು ಹೇಳಿಕೊಂಡಿದ್ದರು. ಸಚಿವರು ನಂತರ ತಮ್ಮ ಹೇಳಿಕೆಯನ್ನು ಒಪ್ಪಿಕೊಂಡಿದ್ದು, ತಾವು ಯಾವತ್ತೂ ನಿರ್ದಿಷ್ಟ ವ್ಯಕ್ತಿಯನ್ನು ಕೀಳಾಗಿ ಕಾಣುವ ಉದ್ದೇಶ ಹೊಂದಿರಲಿಲ್ಲ, ಆದರೆ ಕೆಲವು ಪಿಳ್ಳೈ ಕುಟುಂಬಗಳನ್ನು ಮಾತ್ರ ಕೀಳಾಗಿ ಕಾಣುವ ಉದ್ದೇಶ ಹೊಂದಿದ್ದರು ಎಂದು ಹೇಳಿದ್ದಾರೆ. ವಿಜಯನ್ ಅವರು ನಟರಾಜರ ಹೆಸರು ಸಹ ನೆನಪಿಲ್ಲ ಎಂದು ಹೇಳಿ ವಿವಾದಗಳನ್ನು ಸ್ಪಷ್ಟಪಡಿಸಿದರು. ವಿರೋಧ ಪಕ್ಷವಾದ ಭಾರತೀಯ ರಾಷ್ಟ್ರೀಯ ಕಾಂಗ್ರೆಸ್, ಕೇರಳ ಸಿಎಂ ಅವರ ಹೇಳಿಕೆಗೆ ಸಂಬಂಧಿಸಿದಂತೆ ಅವರ ರಾಜೀನಾಮೆಗೆ ಒತ್ತಾಯಿಸಿದ್ದು, ಇದು ವ್ಯಾಪಕ ವಿವಾದಕ್ಕೆ ಕಾರಣವಾಯಿತು. ..
```


### BhashaWiki — Marathi

absent

No folder for Marathi under `datasets/bhashawiki/`.

### BhashaWiki — Gujarati

- **S3 key:** `datasets/bhashawiki/guj_Gujr/train-001-of-11.parquet`
- **Column:** `text`
- **Document id:** `63047548` (column `id`)
- **Character length:** 2,031

The first 700 characters, then the last 700. 631 characters were cut from the middle.

```
પી. એસ. નટરાજ પિલ્લઈ (માર્ચ 1891-1966) એક ભારતીય રાજકારણી, સ્વાતંત્ર્ય સેનાની અને 1962માં યોજાયેલી ત્રીજી લોકસભાની ચૂંટણી દરમિયાન સંસદના સભ્ય હતા. તેમણે 1948માં દિલ્હીમાં ત્રાવણકોર સરકારના સલાહકાર અને 1954થી 1955 સુધી ત્રાવણકોર-કોચીન રાજ્યના નાણાં મંત્રી તરીકે સેવા આપી હતી. જીવન અને પૃષ્ઠભૂમિ પી. એસ. નટરાજાનો જન્મ માર્ચ 1891માં કેરળના અલાપ્પુઝા જિલ્લામાં થયો હતો. તેઓ મૂળરૂપે 1962માં સ્વતંત્ર રીતે સંસદના સભ્ય તરીકે ચૂંટાયા હતા; બાદમાં, તેમણે કોંગ્રેસ, ભારતીય સમાજવાદી પક્ષ અને પ્રજા સમાજવાદી પક્ષ સાથે તેમના રાજકીય જોડાણોની સ્થાપના કરી હતી. ભારતની આઝાદી પહેલાં, તેઓ 1946માં ત્રાવણકોર બંધારણ સુધારણા સમિતિના સભ્ય હતા. તેમની કારકિર્દી દરમિયાન, તેઓ 1952 થી 1953 સુધી ત્રાવણકોર મણિગામ કરમ સમિતિ, 1956 
```


631 characters cut

```
્રો હતા. નટરાજ ભારતીય વિદ્વાન મનોમનિયમ પી. સુંદરમ પિલ્લઈના પુત્ર હતા, જેઓ વ્યાવસાયિક રીતે પ્રોફેસર મનોમનિયમ સુંદરમ પિલ્લઈ તરીકે જાણીતા હતા, જેઓ કેરળ સ્થિત એક કોલેજમાં શિક્ષક હતા. વિવાદો 2017માં કેરળના મુખ્યમંત્રી પિનારાઈ વિજયને પી. એસ. નટરાજ પિલ્લઈ વિશે વાંધાજનક ટિપ્પણી કરવાનો દાવો કર્યો હતો. મંત્રીએ પાછળથી આ ટિપ્પણીને સ્વીકારી હતી અને કહ્યું હતું કે તેમનો ઈરાદો ક્યારેય કોઈ ચોક્કસ વ્યક્તિનું અપમાન કરવાનો નહોતો, પરંતુ માત્ર કેટલાક પિલ્લઈ પરિવારોનું અપમાન કરવાનો હતો. વિજયને એ ટાંકીને વિવાદોની સ્પષ્ટતા કરી હતી કે તેમને નટરાજનું નામ પણ યાદ નહોતું. વિપક્ષી દળ ભારતીય રાષ્ટ્રીય કોંગ્રેસે કેરળના મુખ્યમંત્રીના નિવેદનને લઈને તેમના રાજીનામાની માંગ કરી હતી, જેના કારણે તેઓ વ્યાપક વિવાદમાં મુકાયા હતા. તા.
```


### Cosmopedia — Hindi

- **S3 key:** `translations/Cosmopedia-v2/Krutrim/krutrim-cosmopedia-v2-decoupled-v4-20260905/language=hin_Deva/source=0c2b4d7f39a75370128f69a68b722315b7a913a2b9a9bd18510e6ca89cac1716/chunk=02dbd057a8502613cd8e3a443741b70f2bc06a9e5066fd78d735b320a8dc96a6/translated_documents.parquet`
- **Column:** `translation`
- **Document id:** `0` (column `document_id`)
- **Character length:** 3,468
- **Note:** v4. v5 has no folder for this language, so this is a v4-only source.
- **Columns checked:** `translation` is the translated text. `translation_sha256` is a 64-character hex digest.

The first 700 characters, then the last 700. 2,068 characters were cut from the middle.

```
 अध्याय 10: भांग के साथ बागवानी-सही तनाव का चयन करना

क्या आपने कभी भांग के साथ बागवानी के बारे में सुना है? जिस तरह हम घर पर फूलों और सब्जियों की देखभाल करते हैं, उसी तरह मारिजुआना को भी प्यार और ध्यान की आवश्यकता होती है ताकि यह स्वस्थ पौधों में विकसित हो सके! अपना खुद का भांग उद्यान शुरू करते समय विचार करने के लिए एक महत्वपूर्ण बात यह है कि सही तनाव का चयन करना है। लेकिन इसका सही मतलब क्या है? चलो अंदर गोता लगाते हैं और एक साथ पता लगाते हैं!

**भांग की जड़ों को समझना**

कल्पना कीजिए कि विभिन्न प्रकार के फलों से भरे एक विशाल ग्रीनहाउस के अंदर चलना-कुछ में रसदार लाल मांस होता है (जैसे टमाटर), जबकि अन्य लंबे और हरे (जैसे खीरे) हो सकते हैं। इसी तरह, दुनिया भर में सैकड़ों अलग-अलग भांग * उपभेदो
```


2,068 characters cut

```
और बाहर दोनों अपेक्षाकृत तेजी से बढ़ता है।

2. **उत्तरी रोशनी**: अपने लचीलेपन और कम से कम सही परिस्थितियों में भी पनपने की क्षमता के लिए पहचाने जाने वाले, उत्तरी रोशनी एक शुद्ध इंडिका तनाव है। इसकी मिट्टी की, मसालेदार सुगंध एक शांत प्रभाव की ओर ले जाती है, जिससे यह रात के समय उपयोग के लिए उपयुक्त हो जाती है।

3. **जैक हेरर**: एक महान भांग कार्यकर्ता के नाम पर नामित, जैक हेरर एक बहुमुखी सैटिवा-प्रमुख संकर है। सतर्कता और उत्साह को बढ़ावा देने के लिए प्रसिद्ध, यह तनाव एक पाइन-साइट्रस सुगंध का दावा करता है और घने, हल्के हरे कलियों का उत्पादन करता है।

याद रखें, सही भांग तनाव चुनना सफल खेती और सुखद अंतिम परिणामों की नींव सेट करता है। इसलिए अपना समय विकल्पों की खोज करें और अपने लिए सही फिट ढूंढें!
```


### Cosmopedia — Bengali

- **S3 key:** `translations/Cosmopedia-v2/Krutrim/krutrim-cosmopedia-v2-decoupled-v4-20260905/language=ben_Beng/source=1704bc31ef3c6bc88f0e362eb1421820ce0196eaa33dbee1f1c5085ad2382204/chunk=0acd4e3a0e2960bf2f50972fd89f51e936287461abd50134c4882a6594f9d38f/translated_documents.parquet`
- **Column:** `translation`
- **Document id:** `0` (column `document_id`)
- **Character length:** 4,145
- **Note:** v4. v5 has no folder for this language, so this is a v4-only source.
- **Columns checked:** `translation` is the translated text. `translation_sha256` is a 64-character hex digest.

The first 700 characters, then the last 700. 2,745 characters were cut from the middle.

````
## পান্ডাস সিরিজে তথ্যের ধরন অনুকূল করা হচ্ছে

এই অধ্যায়ে, আমরা একটি সিরিজের ডেটা প্রকারগুলি ডাউনকাস্ট করে পাণ্ডাতে মেমরি ব্যবহারকে অনুকূল করার একটি কৌশল অন্বেষণ করব। এই কৌশলটি বিশেষত বড় ডেটাসেটগুলির সাথে কাজ করার সময় কার্যকর, কারণ এটি ডেটা সংরক্ষণের জন্য প্রয়োজনীয় মেমরির পরিমাণ উল্লেখযোগ্যভাবে হ্রাস করতে পারে।

কোডটিতে ডুব দেওয়ার আগে, প্রথমে ডাউনকাস্টিং মানে কী তা বোঝা যাক। ডাউনকাস্টিং হল একটি পরিবর্তনশীলকে বৃহত্তর ডেটা টাইপ থেকে ছোটতে রূপান্তর করার প্রক্রিয়া। উদাহরণস্বরূপ, আমরা পাণ্ডাদের একটি সিরিজকে ডাউনকাস্ট করতে পারি `float64` করতে `float32`যা ডেটা সংরক্ষণের জন্য প্রয়োজনীয় মেমরির পরিমাণ অর্ধেক করে দেবে।

এখন, কোডটি দেখুনঃ

```python
import pandas as pd
import numpy as np

def c
````


2,745 characters cut

````
_downcasted.dtype)
```

এই কোডটি একটি পাণ্ডাস সিরিজ তৈরি করে `s` পাঁচটি পূর্ণসংখ্যা মান সহ এবং তারপরে সিরিজটি ব্যবহার করে ডাউনকাস্ট করুন `downcast_to_smallest_dtype` ফাংশন। ফলস্বরূপ সিরিজ `s_downcasted` একটি ডেটা টাইপ আছে `int8`, যা সবচেয়ে ছোট ডেটা টাইপ যা সিরিজের মানগুলিকে সঠিকভাবে উপস্থাপন করতে পারে।

সংক্ষেপে, ডাউনকাস্টিং পাণ্ডাতে মেমরি ব্যবহারকে অনুকূল করার জন্য একটি শক্তিশালী কৌশল। একটি সিরিজকে সবচেয়ে ছোট সম্ভাব্য ডেটা টাইপে রূপান্তর করে যা সিরিজের মানগুলিকে সঠিকভাবে উপস্থাপন করতে পারে, আমরা ডেটা সংরক্ষণের জন্য প্রয়োজনীয় মেমরির পরিমাণ উল্লেখযোগ্যভাবে হ্রাস করতে পারি। দ্য `downcast_to_smallest_dtype` ফাংশন স্বয়ংক্রিয়ভাবে এই অপ্টিমাইজেশন সম্পাদন করার একটি সুবিধাজনক উপায় প্রদান করে।
````


### Cosmopedia — Tamil

- **S3 key:** `translations/Cosmopedia-v2/Krutrim/krutrim-cosmopedia-v2-decoupled-v4-20260905/language=tam_Taml/source=070d4f2cb2d991a6c53de9105a9afeda92876fe786106c666831a33fcdb8d773/chunk=0055abca36bdcfd1357d574b4860c1188fd5663ebe72ec4de5378eb15ab07895/translated_documents.parquet`
- **Column:** `translation`
- **Document id:** `0` (column `document_id`)
- **Character length:** 2,986
- **Note:** v4. v5 has no folder for this language, so this is a v4-only source.
- **Columns checked:** `translation` is the translated text. `translation_sha256` is a 64-character hex digest.

The first 700 characters, then the last 700. 1,586 characters were cut from the middle.

```
 அத்தியாயம் 7: பிழை பகுப்பாய்வு மற்றும் பரப்புதலைப் புரிந்துகொள்வது

உங்கள் வகுப்பறை கதவின் அகலத்தை அளவிட முயற்சிக்கிறீர்கள் என்று கற்பனை செய்து பாருங்கள். இதைச் செய்ய நீங்கள் ஒரு ஆட்சியாளரைப் பயன்படுத்தலாம், ஆனால் கதவு சட்டகத்துடன் ஆட்சியாளரின் விளிம்பை எவ்வளவு கவனமாக வரிசைப்படுத்தினாலும், உங்கள் அளவீட்டில் எப்போதும் சில நிச்சயமற்ற தன்மை இருக்கும். ஒருவேளை ஆட்சியாளரின் முடிவு சரியாக நேராக இருக்காது, அல்லது விளிம்பு எங்கே வரிசையாக நிற்கிறது என்பதைப் பார்ப்பது கடினம். நீங்கள் எவ்வளவு கவனமாக இருந்தாலும், உங்கள் அளவீட்டில் எப்போதும் ஒரு சிறிய பிழை இருக்கும்.

கணிதம் மற்றும் அறிவியலில், நாம் பெரும்பாலும் சில பிழைகளைக் கொண்ட அளவீடுகளுடன் வேலை செய்ய வேண்டும். சிக்கல்களைத் தீர்க்க கணினிகள் போன்ற ஆட
```


1,586 characters cut

```
Δஎல்/எல்) ^ 2 + (Δடபிள்யூ/டபிள்யு) ^ 2]
= (8 m × 4 m) × sqrt [(0.5 m / 8 m) ^ 2 + (0.3 m / 4 m) ^ 2]
± 32 m^2 × சதுர [0.0625 + 0.0225]
± 32 m^2 × சதுர [0.085]
± 32 m^2 × 0.2915
± 9.32 m^2

எனவே, பரப்பளவைக் கணக்கிடுவதில் அதிகபட்ச பிழை தோராயமாக 9.32 சதுர மீட்டர் ஆகும்.

பிழை பகுப்பாய்வு மற்றும் பரப்புதலைப் புரிந்துகொள்வது சிறந்த சிக்கல் தீர்வுகளாக மாற உதவுகிறது, ஏனென்றால் இது எங்கள் பதில்கள் எங்கள் தேவைகளுக்கு போதுமான துல்லியமானவையா என்பது குறித்து தகவலறிந்த முடிவுகளை எடுக்க அனுமதிக்கிறது. பிழைகளை எவ்வாறு அளவிடுவது மற்றும் நிர்வகிப்பது என்பதைக் கற்றுக்கொள்வதன் மூலம், நமது கணிதத் திறன்களில் நம்பிக்கையை வளர்க்கலாம் மற்றும் நமது வாழ்நாள் முழுவதும் நமக்கு நன்றாக சேவை செய்யும் திறன்களை வளர்க்கலாம்.
```


### Cosmopedia — Telugu

- **S3 key:** `translations/Cosmopedia-v2/Krutrim/krutrim-cosmopedia-v2-decoupled-v4-20260905/language=tel_Telu/source=1a672a44e013caf7989deab521406570d80df8b4af5944d95c5fa648097be787/chunk=0a59c12ea1e7d0af534b35b95a01935d413470266d92a1cf7777a05a1fdde14d/translated_documents.parquet`
- **Column:** `translation`
- **Document id:** `0` (column `document_id`)
- **Character length:** 5,473
- **Note:** v4. v5 has no folder for this language, so this is a v4-only source.
- **Columns checked:** `translation` is the translated text. `translation_sha256` is a 64-character hex digest.

The first 700 characters, then the last 700. 4,073 characters were cut from the middle.

```
 పిండం అభివృద్ధి అనేది ఒక సంక్లిష్టమైన మరియు మనోహరమైన ప్రక్రియ, ఇందులో ఫలదీకరణ గుడ్డు పూర్తిగా ఏర్పడిన పిండంగా రూపాంతరం చెందుతుంది. ఈ ప్రక్రియ వేగవంతమైన పెరుగుదల మరియు స్థిరమైన మార్పుతో వర్గీకరించబడుతుంది, ఇది వైద్య పిండ శాస్త్రంలో సవాలుగా ఇంకా కీలకమైన అధ్యయన రంగంగా మారుతుంది. ఈ కోర్సు యూనిట్లో, పిండం అభివృద్ధి యొక్క చిక్కులను లోతుగా పరిశీలిస్తాము, ఇందులో ఉన్న కీలక దశలు మరియు నిర్మాణాలను అన్వేషిస్తాము అలాగే వాటిని అధ్యయనం చేయడానికి ఉపయోగించే సాధనాలు మరియు పద్ధతులను అన్వేషిస్తాం.

ప్రారంభించడానికి, పిండం అభివృద్ధి గురించి బోధన మరియు నేర్చుకోవడంలో అంతర్లీనమైన సవాళ్లను పరిశీలిద్దాం. సారంలో పేర్కొన్నట్లుగా, అభివృద్ధి చెందుతున్న పిండానికి చెందిన చిన్న పరిమాణం మరియు నిరంతరం అభివృద్ధి చెందుతూ ఉండే 
```


4,073 characters cut

```
 వాస్తవిక పిండాలను ఉత్పత్తి చేయడానికి అనుమతిస్తుంది, ఇది జాతుల అంతటా పదనిర్మాణ వైవిధ్యాల యొక్క క్రియాత్మక ప్రాముఖ్యతను అన్వేషించడానికి వీలు కల్పిస్తుంది.

ముగింపులో, పిండం అభివృద్ధి వైద్య పిండ శాస్త్రంలో పరిశోధన యొక్క గొప్ప మరియు బహుముఖ డొమైన్ను సూచిస్తుంది. ఈ ప్రక్రియను రూపొందించే జన్యు, ఎపిజెనెటిక్ మరియు పర్యావరణ కారకాల మధ్య క్లిష్టమైన పరస్పర చర్యను పరిశీలించడం ద్వారా, పరిశోధకులు మానవ జీవితకాలం అంతటా జీవితం యొక్క మూలాలు మరియు ఆరోగ్య నిర్వహణపై ప్రాథమిక అంతర్దృష్టులను పొందడానికి నిలబడతారు. అంతేకాకుండా, శాస్త్రీయ పరిశోధనలో ముందంజలో కొత్త ఆవిష్కరణలు కొనసాగుతున్నందున, అభ్యాసకులు మరియు శిక్షణ పొందినవారు ఈ ఉత్తేజకరమైన రంగంలో అభివృద్ధి చెందుతున్న పోకడలు మరియు పరిణామాలకు అనుగుణంగా ఉండటం చాలా అవసరం.
```


### Cosmopedia — Kannada

- **S3 key:** `translations/Cosmopedia-v2/Krutrim/krutrim-cosmopedia-v2-decoupled-v5-20260906/language=kan_Knda/source=12edd356ada9c952b670f1358bef21dd0ce9c2924cf688915fb000c574194fc3/chunk=0156f2983dd701670b31aa6005d9a68c052675f7ab0a04f65aeec6dbca16da1d/translated_documents.parquet`
- **Column:** `translation`
- **Document id:** `0` (column `document_id`)
- **Character length:** 3,327
- **Note:** v5. This language has a v5 folder, so v4 was not opened.
- **Columns checked:** `translation` is the translated text. `translation_sha256` is a 64-character hex digest.

The first 700 characters, then the last 700. 1,927 characters were cut from the middle.

```
 ನನ್ನ ಮಗ ಶಾಲೆಯಿಂದ ಮನೆಗೆ ಬಂದ ಒಂದು ದುರದೃಷ್ಟಕರ ದಿನದವರೆಗೂ ನಾನು ದ್ಯುತಿಸಂಶ್ಲೇಷಣೆಯ ಬಗ್ಗೆ ಹೆಚ್ಚು ಯೋಚಿಸಲಿಲ್ಲ, ತನ್ನ ವಿಜ್ಞಾನ ಯೋಜನೆಯ ಬಗ್ಗೆ ಉತ್ಸಾಹದಿಂದ ಸ್ಫೋಟಗೊಂಡಿದ್ದೇನೆ. ದ್ಯುತಿಸಂಶ್ಲೇಷಣೆಯ ಪ್ರಕ್ರಿಯೆಯನ್ನು ಪ್ರದರ್ಶಿಸಲು ಅವರು ವಿವಿಧ ರೀತಿಯ ಸಸ್ಯಗಳಿಂದ ತುಂಬಿದ ಭೂಚರಾಲಯವನ್ನು ರಚಿಸಲು ಬಯಸಿದ್ದರು. ಮೊದಲಿಗೆ, ಅವರು ಶೈಕ್ಷಣಿಕವಾದ ಯಾವುದನ್ನಾದರೂ ಆಸಕ್ತಿ ತೋರಿಸಿದ ಬಗ್ಗೆ ನನಗೆ ಸಂತೋಷವಾಯಿತು, ಆದ್ದರಿಂದ ನಾನು ಅವರಿಗೆ ಸಹಾಯ ಮಾಡಲು ಒಪ್ಪಿಕೊಂಡೆ. ಈ ಸರಳ ಯೋಜನೆಯು ನಮ್ಮ ಜೀವನವನ್ನು ಶಾಶ್ವತವಾಗಿ ಎಷ್ಟು ಬದಲಾಯಿಸುತ್ತದೆ ಎಂದು ನನಗೆ ತಿಳಿದಿರಲಿಲ್ಲ.

ಪರಿಪೂರ್ಣ ಭೂಚರಾಲಯಕ್ಕಾಗಿ ವಸ್ತುಗಳನ್ನು ಸಂಶೋಧಿಸಲು ಮತ್ತು ಸಂಗ್ರಹಿಸಲು ನಾವು ಗಂಟೆಗಳ ಕಾಲ ಕಳೆದಿದ್ದೇವೆ. ಪಾಚಿಗಳು, ಜರೀಗಿಡಗಳು, ಚಿಕಣಿ ರಬ್ಬರ್ ಮರ-ನನ್ನ ಮಗ ಎಚ್ಚರಿಕೆಯಿಂದ ವಿವಿಧ ಸಸ್ಯಗಳನ್ನು ಆಯ್ಕೆ ಮಾಡಿಕೊಂಡನು. ನಾವು ದೊಡ್ಡ ಗಾಜಿನ ಧಾರಕದಲ್ಲಿ ಮಣ್ಣು, ಉಂಡೆಗಳು ಮತ್
```


1,927 characters cut

```
ಕಾರಿ ಬ್ಲೂಸ್ ಮತ್ತು ಕೆನ್ನೇರಳೆ ಬಣ್ಣಗಳನ್ನು ಬದಲಿಸಿ ಮರಳಿದವು.

ಈ ಅನುಭವದ ಮೂಲಕ, ಜೀವನವು ಅಭಿವೃದ್ಧಿ ಹೊಂದಲು ಅಗತ್ಯವಾದ ಸೂಕ್ಷ್ಮ ಸಮತೋಲನಕ್ಕಾಗಿ ನಾನು ಸಂಪೂರ್ಣ ಹೊಸ ಮೆಚ್ಚುಗೆಯನ್ನು ಗಳಿಸಿದೆ. ದ್ಯುತಿಸಂಶ್ಲೇಷಣೆಯು, ನೇರವಾದಂತೆ ತೋರುತ್ತದೆಯಾದರೂ, ಬೆಳಕು, ನೀರು ಮತ್ತು ಇಂಗಾಲದ ಡೈಆಕ್ಸೈಡ್ ನಡುವಿನ ನಂಬಲಾಗದಷ್ಟು ಸಂಕೀರ್ಣವಾದ ನೃತ್ಯವಾಗಿದೆ. ಆ ಸಾಮರಸ್ಯವನ್ನು ಹಾಳುಮಾಡುತ್ತದೆ ಮತ್ತು ಅವ್ಯವಸ್ಥೆ ಉಂಟಾಗುತ್ತದೆ. ಈಗ ನಾನು ಸೂರ್ಯನ ಬೆಳಕಿನಲ್ಲಿ ಹಸಿರು ಎಲೆಗಳುಳ್ಳ ಸಸ್ಯವನ್ನು ನೋಡಿದಾಗಲೆಲ್ಲಾ, ಪ್ರಕೃತಿಯ ಸ್ಥಿತಿಸ್ಥಾಪಕತ್ವವನ್ನು ಮಾತ್ರವಲ್ಲದೆ ಅದರ ಸೂಕ್ಷ್ಮತೆಯನ್ನೂ ನನಗೆ ನೆನಪಿಸಿಕೊಳ್ಳಲಾಗುತ್ತದೆ. ನಮ್ಮ ಕ್ರಿಯೆಗಳು, ಎಷ್ಟೇ ಉದ್ದೇಶಿತವಾಗಿದ್ದರೂ, ದೂರಗಾಮಿ ಪರಿಣಾಮಗಳನ್ನು ಬೀರಬಹುದು. ಆದ್ದರಿಂದ ಗೋಚರ ಮತ್ತು ಸೂಕ್ಷ್ಮ ರೂಪಗಳಲ್ಲಿ ಹೇರಳವಾಗಿರುವ ಪವಾಡಗಳನ್ನು ಗೌರವಿಸಿ ಮತ್ತು ಸಂರಕ್ಷಿಸಿ, ಈ ಭೂಮಿಯ ಮೇಲೆ ಲಘುವಾಗಿ ನಡೆಯಲು ಪ್ರಯತ್ನಿಸೋಣ.
```


### Cosmopedia — Marathi

- **S3 key:** `translations/Cosmopedia-v2/Krutrim/krutrim-cosmopedia-v2-decoupled-v5-20260906/language=mar_Deva/source=09b2e3f7a5a90612bfeda8e69b047ed9bb4811efa502b1d43740c6dd830b5c07/chunk=11d1bcaf56495c5989963eec76d915768a1642cfa00a07f2f750997b59c46c58/translated_documents.parquet`
- **Column:** `translation`
- **Document id:** `0` (column `document_id`)
- **Character length:** 3,288
- **Note:** v5. This language has a v5 folder, so v4 was not opened.
- **Columns checked:** `translation` is the translated text. `translation_sha256` is a 64-character hex digest.

The first 700 characters, then the last 700. 1,888 characters were cut from the middle.

```
 अध्याय 5: कर्लिंग धोरण आणि युक्त्या-तुमच्या विरोधकांना बर्फावर पछाडणे!

तुम्ही कधी कर्लर्स बर्फावर दगड चढवत पाहिले आहेत का, तर त्यांचे सहकारी समोर रागाने झाडू मारतात? रणनीती, कौशल्य आणि सांघिक कार्य यांचा मेळ घालणारा हा एक आकर्षक हिवाळी खेळ आहे! कर्लिंगच्या रोमांचक जगात प्रवेश करूया आणि काही विजयी धोरणे आणि डावपेच जाणून घेऊया.

**विभाग 1: कर्लिंगची मूलभूत तत्त्वे**

कर्लिंगमध्ये, प्रत्येकी चार खेळाडूंचे दोन संघ वळून जड ग्रॅनाइट दगड (ज्याला खडक असेही म्हणतात) 'घर' नावाच्या गोलाकार लक्ष्य क्षेत्राकडे सरकवतात. प्रत्येक संघात आठ दगड असतात आणि दोन्ही संघांनी त्यांचे सर्व दगड फेकल्यानंतर तुमच्या प्रतिस्पर्ध्यापेक्षा घराच्या मध्यभागी अधिक दगड ठेवणे हे उद्दिष्ट आहे. खेळ सहसा दहा टोकांवर खेळले जातात
```


1,888 characters cut

```
. तापमान, आर्द्रता आणि देखभाल यासारख्या वेगवेगळ्या परिस्थितींमुळे प्रत्येक बर्फाचा पृष्ठभाग वेगळा असतो. सूक्ष्म बदल दगडांच्या हालचालींवर परिणाम करतात, ज्यामुळे बर्फ वाचणे यशासाठी महत्त्वाचे ठरते.

शेवटी, संघातील सदस्यांमधील संवाद हे सुनिश्चित करतो की प्रत्येकाला त्यांची भूमिका समजते आणि त्यानुसार अंमलबजावणी होते. स्किप शॉट निवड, स्वीपिंग तीव्रता आणि दगड वितरण गतीबद्दल स्पष्ट सूचना देतात. यशस्वी परिणामांमध्ये सांघिक गतिशीलता महत्त्वपूर्ण भूमिका बजावते!

तर तिथे तुमच्याकडे ते आहे-कर्लिंग रणनीती आणि डावपेचांची ओळख! या संकल्पनांचा सराव आणि समज यामुळे तुम्ही देखील बर्फाच्या रिंकवर एक प्रचंड शक्ती बनू शकता. लक्षात ठेवा, कोणत्याही खेळात प्रभुत्व मिळविण्यासाठी संयम, समर्पण आणि वाटेत भरपूर मजा लागते!
```


### Cosmopedia — Gujarati

- **S3 key:** `translations/Cosmopedia-v2/Krutrim/krutrim-cosmopedia-v2-decoupled-v4-20260905/language=guj_Gujr/source=0ac9a4c2b9faaa5368f8a93b1247ea1af025f33ce6e97b8f43953363b3751a7f/chunk=040376cd004f62fdfc24312b27b37e268a075ac9727ac6bb8d9b8ff831f1ddbf/translated_documents.parquet`
- **Column:** `translation`
- **Document id:** `0` (column `document_id`)
- **Character length:** 2,232
- **Note:** v4. v5 has no folder for this language, so this is a v4-only source.
- **Columns checked:** `translation` is the translated text. `translation_sha256` is a 64-character hex digest.

The first 700 characters, then the last 700. 832 characters were cut from the middle.

```
આધુનિક ઇઝરાયેલી સંસ્કૃતિ અને માધ્યમોમાં તમારી યાત્રામાં આપનું સ્વાગત છે! આજે આપણે કેટલાક રસપ્રદ પુસ્તકો શોધીશું જે સમકાલીન ઇઝરાયેલી સમાજ અને તેના પડોશીઓ સાથેની તેની ક્રિયાપ્રતિક્રિયાઓ પર પ્રકાશ પાડે છે. આ પુસ્તકો ઇઝરાયેલ અને કબજામાં આવેલા પ્રદેશોમાં જીવનના વિવિધ પાસાઓ આવરી લે છે, જે આપણને વિવિધ પરિપ્રેક્ષ્યો અને અનુભવોમાં મૂલ્યવાન આંતરદૃષ્ટિ પ્રદાન કરે છે. ખાસ કરીને, આપણે આ વાર્તાઓ ઇતિહાસ, રાજકારણ અને વિવિધ સંસ્કૃતિઓથી ભરેલા પ્રદેશમાં રહેવાની જટિલતાઓને સમજવામાં કેવી રીતે મદદ કરે છે તેના પર ધ્યાન કેન્દ્રિત કરીશું.

ચાલો કેટલાક લેખકોની રજૂઆત કરીને શરૂઆત કરીએ જેમણે ઇઝરાયેલ અને પેલેસ્ટાઇન સાથેના તેમના વ્યક્તિગત સંબંધો વિશે લખ્યું છે. નાહલા અબ્દો "કેદની ક્રાંતિથી ગ્રાન્ડ ગાઝા જેલ" (2014) માં તેના
```


832 characters cut

```
ું હતું, જેમાં નોંધપાત્ર લેખકોના નિબંધો છે, જે વ્યવસાય હેઠળ રહેતા લોકો દ્વારા સામનો કરવામાં આવતા દૈનિક સંઘર્ષોની ચર્ચા કરે છે.

અમે જાસ્મીન ડોનાહાયેની "લોઝિંગ ઇઝરાયેલ" (2015) પણ રજૂ કરવા માંગીએ છીએ. ઓળખ અને વફાદારીના પ્રશ્નો સાથે સંઘર્ષ કરતા બ્રિટિશ યહૂદી તરીકે, ડોનાહાયે વિશ્વભરના યહૂદી લોકો અને ઇઝરાયેલ વચ્ચેના જટિલ સંબંધોમાં અનન્ય સમજ પ્રદાન કરે છે. બેન એહરેનરિચની "વસંતનો માર્ગઃ પેલેસ્ટાઇનમાં જીવન અને મૃત્યુ" (2016) વાચકોને પશ્ચિમ કાંઠે ઘનિષ્ઠ મુસાફરી પર લઈ જાય છે, જ્યાં તેઓ દમન સામે લડતી અને આત્મ-નિર્ધારણ માટે પ્રયાસ કરતી વ્યક્તિઓને મળે છે.

વધુમાં, સિથિયા ફ્રેન્કલિન, ગેરી ફીલ્ડ્સ અને અન્ય દ્વારા સંપાદિત "લાઇફ ઇન ઓક્યુપાઇડ પેલેસ્ટાઇનઃ અ સ્પેશિયલ ઇશ્યુ ઓફ બાયોગ્રાફી" (2014) જેવા સંગ્રહો છે.
```


### Indic HQ-synthetic — Hindi

- **S3 key:** `translations/Cosmopedia-v2/Krutrim/krutrim-nemotron-cc-v21-hq-synth-v1-20260906/language=hin_Deva/source=152b99982edf6d2f3846da7761e32c9ddbea67fc5ee68af2bf93e19b80168ddd/chunk=08cad0315f5ddbe80c2be95e1a0d7749c9180b138bdf8db22a777c1f52b967cf/translated_documents.parquet`
- **Column:** `translation`
- **Document id:** `0` (column `document_id`)
- **Character length:** 1,750
- **Columns checked:** `translation` is the translated text. `translation_sha256` is a 64-character hex digest.

The first 700 characters, then the last 700. 350 characters were cut from the middle.

```
धोखेबाज़ों को एक उचित सौदा मिलता है लेकिन अंत में दूसरों को धोखा देता है। वे छोटे पैमाने पर काम कर सकते हैं, जैसे कि एक स्ट्रीट कॉन कलाकार, या बड़े पैमाने पर, जैसे एक कॉर्पोरेट धोखेबाज।  

"धोखेबाज" का उपयोग करने वाले वाक्यों के उदाहरणों में शामिल हैंः धोखेबाज ने अपने मुवक्किल के निवेश को दोगुना करने का वादा किया लेकिन पैसे के साथ गायब हो गया; नकली दान चलाने वाले धोखेबाज को आखिरकार पकड़ लिया गया; चालाक धोखेबाज अपने पास की संपत्ति बेचने के लिए जाली दस्तावेजों का उपयोग करता था; एक व्यावसायिक भागीदार को धोखेबाज बताया गया; धोखेबाज बचत चोरी करने से पहले विश्वास हासिल करने के लिए आकर्षण का उपयोग करते थे; एक कुख्यात धोखेबाज कई राज्यों में वित्तीय तबाही का कारण बना; एक बुजुर्ग जोड़े को धोखा दिया गया
```


350 characters cut

```
िसमें अक्सर व्यक्तिगत लाभ या हेरफेर के उद्देश्य से सूक्ष्म और गुप्त तरीके शामिल होते हैं।  

"परोपकारी" एक क्रियाविशेषण है जो उन कार्यों का वर्णन करता है जो निस्वार्थता, दया और दूसरों के कल्याण के लिए चिंता दिखाते हैं, जिसमें व्यक्तिगत हितों पर दूसरों की मदद करने पर ध्यान केंद्रित किया जाता है।  

"हॉबनोब" लोगों के साथ सामाजिक या मेल खाने को संदर्भित करता है, विशेष रूप से उच्च स्थिति या प्रभाव वाले, अक्सर रिश्ते बनाने, पक्ष प्राप्त करने या नेटवर्क बनाने के लिए आकस्मिक बातचीत शामिल करते हैं।  

"मताधिकार" का अर्थ है राजनीतिक चुनावों में मतदान का अधिकार, एक मौलिक लोकतांत्रिक विशेषाधिकार जो नागरिकों को प्रतिनिधियों को चुनने या जनमत संग्रह के माध्यम से निर्णय लेने में भाग लेने की अनुमति देता है।
```


### Indic HQ-synthetic — Bengali

- **S3 key:** `translations/Cosmopedia-v2/Krutrim/krutrim-nemotron-cc-v21-hq-synth-v1-20260906/language=ben_Beng/source=08d49d022bea6d1418e481260179cdd7767dd8d891efade37c5471374432ddc6/chunk=0e4b2a43f2ece7944a4e4ed7e26f653dc06d91a862751b4b34d7daa63e77d02d/translated_documents.parquet`
- **Column:** `translation`
- **Document id:** `0` (column `document_id`)
- **Character length:** 2,026
- **Columns checked:** `translation` is the translated text. `translation_sha256` is a 64-character hex digest.

The first 700 characters, then the last 700. 626 characters were cut from the middle.

```
অবশ্যই! সহস্রাব্দ উন্নয়ন লক্ষ্যমাত্রা (এমডিজি) এবং টেকসই উন্নয়ন লক্ষ্যমাত্রাগুলি (এসডিজিএস) হল জাতিসংঘের উদ্যোগ যার লক্ষ্য হল বৈশ্বিক চ্যালেঞ্জ মোকাবেলা করা, তবে তারা তাদের দৃষ্টিভঙ্গি, সুযোগ এবং পরিবেশগত শিক্ষার উপর দৃষ্টি নিবদ্ধ করার ক্ষেত্রে ভিন্ন। এমডিজিগুলি 2000 সালে শুরু হয়েছিল যার লক্ষ্য সমাপ্তির তারিখ ছিল 2015. এগুলি আটটি লক্ষ্য নিয়ে গঠিত, যার প্রত্যেকটির নির্দিষ্ট লক্ষ্য দারিদ্র্য হ্রাস, স্বাস্থ্য, শিক্ষা, লিঙ্গ সমতা এবং পরিবেশগত স্থায়িত্বের উপর দৃষ্টি নিবদ্ধ করে। লক্ষ্য 7, পরিবেশগত স্থায়িত্ব নিশ্চিত করা, টেকসই উন্নয়ন সংহতকরণ, পরিবেশ সম্পদের ক্ষতি বিপরীত করা, জীববৈচিত্র্যের ক্ষতি হ্রাস করা এবং পরিষ্কার জল ও স্যানিটেশন অ্যাক্সেস উন্নত করার মতো বিষয়গুলি সম্বোধন করা। যাইহোক, পর
```


626 characters cut

```
মন্বিত পদ্ধতির প্রচার করে। টেকসই উন্নয়নের জন্য শিক্ষা একটি মূল উপাদান, বিশেষ করে লক্ষ্য 4-এ, যার লক্ষ্য হল টেকসই উন্নয়ন, মানবাধিকার, লিঙ্গ সমতা এবং শান্তির শিক্ষার মাধ্যমে টেকসই বিকাশের জন্য প্রয়োজনীয় জ্ঞান এবং দক্ষতা অর্জন করা। এসডিজিগুলি পরিবেশগত শিক্ষার প্রতি আরও সামগ্রিক এবং সমন্বিত পদ্ধতির প্রতিফলন ঘটায় এমডিজির তুলনায়, যা পরিবেশগত স্থায়িত্বকে একটি পৃথক বিষয় হিসাবে বিবেচনা করে এবং এটিকে শিক্ষাগত লক্ষ্যগুলিতে সম্পূর্ণরূপে অন্তর্ভুক্ত করে নি। এসডিজিগুলি একটি বিস্তৃত এবং আরও আন্তঃসংযুক্ত কাঠামো সরবরাহ করে যা পরিবেশগত শিক্ষাকে টেকসই উন্নয়নের সাথে আরও ভালভাবে সংহত করে, যেখানে এমডিজি পরিবেশগত স্থায়িত্বের উপর সংকীর্ণ ফোকাস এবং শিক্ষার উপর কম জোর দিয়ে আরও বিভক্ত পদ্ধতির প্রস্তাব দেয়।
```


### Indic HQ-synthetic — Tamil

- **S3 key:** `translations/Cosmopedia-v2/Krutrim/krutrim-nemotron-cc-v21-hq-synth-v1-20260906/language=tam_Taml/source=08d49d022bea6d1418e481260179cdd7767dd8d891efade37c5471374432ddc6/chunk=060a2ba962012e2571a6e62554b9722fa3cbad776260876845f465740f74a91d/translated_documents.parquet`
- **Column:** `translation`
- **Document id:** `0` (column `document_id`)
- **Character length:** 3,984
- **Columns checked:** `translation` is the translated text. `translation_sha256` is a 64-character hex digest.

The first 700 characters, then the last 700. 2,584 characters were cut from the middle.

```
ஒரு வேட்பாளர் தரவு அலகு இணைக்கப்பட்ட ஒவ்வொரு சுட்டியையும் முன்பு குறியிடப்பட்ட தரவு அலகிலிருந்து தொடர்புடைய சுட்டியுடன் மாற்றுவது ஒவ்வொரு தொடர்புடைய சுட்டியின் குறிப்பு எண்ணிக்கையை அதிகரிப்பதை உள்ளடக்கியது.

9. உரிமைகோரல் 1 இன் படி முறை, இதில் ஒரு வேட்பாளர் தரவு அலகு அடையாளம் காண்பது ஒரு கோப்பு அமைப்பு பொருளின் ரூட் முனையில் ஒரு படைப்பு சோதனைச் சாவடி ஆராய்வதையும், கோப்பு முறை பொருள் ஏதேனும் வேட்பாளர் தரவ அலகுகளைக் கொண்டிருக்கிறதா என்பதை தீர்மானிப்பதையும் உள்ளடக்கியது, குறைந்தபட்சம் ஒரு பகுதியாக உருவாக்கம் சோதனைச் சுட்டி.

10. கோப்பு அமைப்பு பொருள் ஏதேனும் வேட்பாளர் தரவு அலகுகளைக் கொண்டிருக்கிறதா என்பதை தீர்மானிக்கும் முறையின் கூற்று 9 இன் படி, பின்வருவனவற்றை உள்ளடக்கியதுஃ படைப்பு சோதனைச் சாவ
```


2,584 characters cut

```
ான வேட்பாளர் தரவு அலகு (210).

14. ஒரு தரவு சேமிப்பு அமைப்பு கூற்றுப்படி ஒன்று அல்லது அதற்கு மேற்பட்ட கோப்பு அமைப்பு சேவையகங்கள் அடங்கும் 13, மற்றும் ஒரு தகவல் தொடர்பு நெட்வொர்க் வழியாக ஒன்று அல்லது மேற்பட்ட கோப்பை அமைப்பு சேவையகங்களுடன் இணைக்கப்பட்ட கிளையன்ட் கணினிகளின் பன்முகத்தன்மை.

15. ஒரு கணினி நிரல் தயாரிப்பு கணினி படிக்கக்கூடிய நிரல் அறிவுறுத்தல்களை உள்ளடக்கியது, இது ஒரு கோப்பு அமைப்பு சேவையகத்தில் இயங்கும் போது அல்லது ஏற்றப்படும் போது அல்லது ஒரு கோபு அமைப்பு சேவையகத்துடன் இணைக்கப்பட்ட கணினியில் அல்லது ஒன்று அல்லது அதற்கு மேற்பட்ட செயலிகளால் அல்லது கோப்பு கணினி சேவையகத்தின் செயலாக்க அலகுகளால் செயல்படுத்தப்படும் போது, கோப்பு முறைமை சேவையகம் குறைந்தபட்சம் படி ஒரு முறையை செயல்படுத்தும்.
```


### Indic HQ-synthetic — Telugu

- **S3 key:** `translations/Cosmopedia-v2/Krutrim/krutrim-nemotron-cc-v21-hq-synth-v1-20260906/language=tel_Telu/source=23a49b8e903b048defb4c0c70e618d6e6e077a9a12a288064e07be28d7c3ed37/chunk=01a9ed73f4c75b406d33a276d6a03f3f20007e034b481378e71f76c9ef8062a9/translated_documents.parquet`
- **Column:** `translation`
- **Document id:** `0` (column `document_id`)
- **Character length:** 5,952
- **Columns checked:** `translation` is the translated text. `translation_sha256` is a 64-character hex digest.

The first 700 characters, then the last 700. 4,552 characters were cut from the middle.

```
నిర్మాణాత్మక విధానం అభ్యాసకులు వారమంతా తగినంత సాధన పొందేలా చూసుకుంటూ వారి ఈత నైపుణ్యాల యొక్క వివిధ అంశాలపై దృష్టి పెట్టడానికి సహాయపడుతుంది. ప్రాక్టీస్ సెషన్లను ఆసక్తికరంగా ఉంచడానికి, వివిధ రకాల కసరత్తులు మరియు వ్యాయామాలను ఉపయోగించడం ప్రయోజనకరంగా ఉంటుంది. కార్యకలాపాలను మార్చడం ద్వారా, అభ్యాసకులు తమ నైపుణ్యాలను నిరంతరం మెరుగుపరుస్తూ నిమగ్నమై మరియు ప్రేరణ పొందుతారు. ప్రాక్టీస్ సెషన్ల లాగ్ను ఉంచడం దూరాలను నమోదు చేయడం ద్వారా పురోగతిని దృశ్యమానం చేయడానికి సహాయపడుతుంది, సాధన యొక్క భావాన్ని పెంపొందించే సాధన పద్ధతులు మరియు వ్యక్తిగత విజయాలు. కొత్త స్ట్రోక్లో ప్రావీణ్యం పొందడం లేదా మరింత దూరం ఈత కొట్టడం వంటి చిన్న మైలురాళ్లను జరుపుకోవడం ప్రేరణను పెంచుతుంది. సారాంశంలో, ఈతలో స్థిరత్వం మరియు సాధన చాలా ము
```


4,552 characters cut

```
్థితో ఎలా సంకర్షణ చెందుతారో గమనించడం అనుకూలతను నిర్ణయించడంలో సహాయపడుతుంది. బోధకుడు అభ్యాసకుడి లక్ష్యాలను అంచనా వేయగలగాలి మరియు ప్రాథమిక స్ట్రోక్లు, సాంకేతికత లేదా పోటీ తయారీపై దృష్టి సారించాలా వద్దా అనేదానికి అనుగుణంగా పాఠాలను అనుకూలీకరించగలగాలని సూచించారు. సమర్థవంతమైన బోధకులు క్రమం తప్పకుండా అభిప్రాయాన్ని అందిస్తారు, విజయాలను గుర్తిస్తూ మెరుగుదల కోసం ప్రాంతాలను హైలైట్ చేస్తారు. వీడియో విశ్లేషణ వంటి సాధనాలు అభ్యాసకులు వారి సాంకేతికతను బాగా అర్థం చేసుకోవడానికి సహాయపడతాయి. ముగింపులో, సరైన బోధకుడిని ఎంచుకోవడంలో అనుభవం, బోధనా శైలి మరియు వ్యక్తిగతీకరించిన మార్గదర్శకత్వాన్ని అందించే సామర్థ్యాన్ని పరిగణనలోకి తీసుకోవడం ఉంటుంది, ఇవన్నీ మరింత విజయవంతమైన మరియు ఆనందదాయకమైన ఈత ప్రయాణానికి దోహదం చేస్తాయి.
```


### Indic HQ-synthetic — Kannada

absent

No folder for Kannada under `translations/Cosmopedia-v2/Krutrim/krutrim-nemotron-cc-v21-hq-synth-v1-20260906/`.

### Indic HQ-synthetic — Marathi

- **S3 key:** `translations/Cosmopedia-v2/Krutrim/krutrim-nemotron-cc-v21-hq-synth-v1-20260906/language=mar_Deva/source=2190e2f1c1b670498806cf05babe7e9f55d53bb25f37af82791666412b9eea81/chunk=f9bedaf63303a61e7000aaceb941c6b36f18bf34e86a5c8a0f26973d0973eeaf/translated_documents.parquet`
- **Column:** `translation`
- **Document id:** `0` (column `document_id`)
- **Character length:** 1,719
- **Columns checked:** `translation` is the translated text. `translation_sha256` is a 64-character hex digest.

The first 700 characters, then the last 700. 319 characters were cut from the middle.

```
aaclient.dll ही एक डायनॅमिक लिंक लायब्ररी (डीएलएल) आहे जी सॉफ्टवेअर अनुप्रयोग आणि कार्यप्रणालीतील प्रमाणीकरण आणि अधिकृततेसाठी आवश्यक आहे. हे क्रेडेन्शियल्स प्रमाणित करून, प्रवेश नियंत्रणे व्यवस्थापित करून आणि सुरक्षा धोरणे लागू करून वापरकर्त्याचे प्रमाणीकरण हाताळते, जे प्रणाली आणि अनुप्रयोगांच्या सुरक्षित आणि विश्वासार्ह कार्यासाठी महत्त्वपूर्ण आहे.

हे डी. एल. एल नेटवर्क सुरक्षा प्रोटोकॉल, वापरकर्ता खाते व्यवस्थापन आणि प्रवेश नियंत्रण यंत्रणेसह समाकलित करते. हे सुरक्षित संवादाला समर्थन देते आणि सुरक्षा धोरणाची अंमलबजावणी करते. हे विविध प्रणाली संरचनांशी सुसंगत आहे, ज्यात समाविष्ट आहे 32-bit (x32) आणि 64-bit (x64) प्रणाली, तसेच विंडोज सारख्या वेगवेगळ्या विंडोज आवृत्त्या 7, 10, आणि 11. योग्य 
```


319 characters cut

```
या समस्यांचे निराकरण करण्यासाठी, वापरकर्त्यांनी योग्य निर्देशिकेत फाइलची उपस्थिती सत्यापित केली पाहिजे किंवा त्यांच्या प्रणाली आणि विंडोज आवृत्तीशी जुळणाऱ्या विश्वासार्ह स्त्रोताकडून योग्य आवृत्ती डाउनलोड केली पाहिजे.

aaclient.dll च्या योग्य व्यवस्थापनासाठी प्रणालीशी सुसंगतता सुनिश्चित करणे आणि डाउनलोडसाठी विश्वासार्ह स्रोत वापरणे आवश्यक आहे. हे एकत्रीकरण समस्या आणि सुरक्षा जोखीम टाळण्यास मदत करते. या मार्गदर्शक तत्त्वांचे पालन करून, वापरकर्ते प्रणाली स्थिरता आणि सुरक्षा राखू शकतात.

aaclient.dll विनामूल्य डाउनलोड करा.  
ही वेबसाइट आपला ब्राउझिंग अनुभव सुधारण्यासाठी आणि आपल्या सेवा सुधारण्यासाठी कुकीज वापरते. आमच्या साइटचा वापर करून, आपण आमच्या गोपनीयता धोरणानुसार कुकीज वापरण्यास सहमत आहात.
```


### Indic HQ-synthetic — Gujarati

- **S3 key:** `translations/Cosmopedia-v2/Krutrim/krutrim-nemotron-cc-v21-hq-synth-v1-20260906/language=guj_Gujr/source=2190e2f1c1b670498806cf05babe7e9f55d53bb25f37af82791666412b9eea81/chunk=025d90df32e9ae7a4a0c038c726da5515633e91e5945b635415b74b953bfe463/translated_documents.parquet`
- **Column:** `translation`
- **Document id:** `0` (column `document_id`)
- **Character length:** 10,409
- **Columns checked:** `translation` is the translated text. `translation_sha256` is a 64-character hex digest.

The first 700 characters, then the last 700. 9,009 characters were cut from the middle.

```
આ લેખ છબી સંસ્થા અને પુનઃપ્રાપ્તિ પર કૃત્રિમ બુદ્ધિ (AI) ની નોંધપાત્ર અસરની શોધ કરે છે, જેમાં AI દ્રશ્ય ડેટાના મોટા જથ્થાને સંભાળવામાં કાર્યક્ષમતા અને ચોકસાઈમાં કેવી રીતે સુધારો કરે છે તેના પર ભાર મૂકવામાં આવે છે. તે સમજાવે છે કે કેવી રીતે AI કન્વોલ્યુશનલ ન્યુરલ નેટવર્ક્સ (સીએનએન) જેવા અદ્યતન અલ્ગોરિધમ્સનો ઉપયોગ કરીને છબીઓની ટેગિંગ, વર્ગીકરણ અને શોધને સ્વચાલિત કરે છે, જે છબી પુનઃપ્રાપ્તિની ઝડપ અને ચોકસાઈને વધારે છે. આ લખાણ વિવિધ ઉદ્યોગોમાં છબી વ્યવસ્થાપનમાં AI સાધનોને શ્રેષ્ઠ બનાવવા માટેના ભવિષ્યના વલણો અને શ્રેષ્ઠ પ્રથાઓ વિશે ચર્ચા કરતી વખતે માહિતીની ગુણવત્તા અને ગોપનીયતાની ચિંતાઓ જેવા પડકારોને પણ સંબોધિત કરે છે.

છબી સંસ્થા અને પુનઃપ્રાપ્તિ પર AI ની અસર નોંધપાત્ર છે, કારણ કે તે મોટા દ્રશ્ય
```


9,009 characters cut

```
રણાલીઓની કાર્યક્ષમતામાં નોંધપાત્ર સુધારો થશે, જેનાથી વપરાશકર્તાઓ માટે સંબંધિત દ્રશ્ય સામગ્રીને ઝડપથી ઍક્સેસ કરવાનું સરળ બનશે.

AI પ્રગતિઓ સાથે વપરાશકર્તા અપેક્ષાઓ વિકસિત થવાની સંભાવના છે કારણ કે સિસ્ટમો વધુ સચોટ, કાર્યક્ષમ અને વ્યક્તિગત બને છે. જેમ જેમ AIમાં સુધારો ચાલુ રહે છે, તેમ તેમ વપરાશકર્તાઓ વધુ સાહજિક ઇન્ટરફેસો, ઝડપી શોધ પરિણામો અને વધુ સુસંગત ભલામણોની અપેક્ષા રાખી શકે છે. કુદરતી ભાષાના પ્રશ્નોને સમજવાની અને તેનો જવાબ આપવાની ક્ષમતા, વધુ સચોટ છબી ઓળખ સાથે, સંભવિત રીતે વપરાશકર્તા અનુભવ માટે બાર વધારશે. વધુમાં, જેમ જેમ AI દૈનિક કાર્યપ્રવાહમાં વધુ સંકલિત બને છે, તેમ તેમ વપરાશકર્તાઓ સીમલેસ અને સ્વચાલિત ઉકેલોની અપેક્ષા રાખી શકે છે જે મેન્યુઅલ પ્રયત્નો ઘટાડે છે અને ઉત્પાદકતામાં વધારો કરે છે.
```


### Fact-Seeking Indic — Hindi

- **S3 key:** `translations/Nemotron-Pretraining-Specialized-v1.2/Fact-Seeking/indictrans2-en-indic-dist-200M-beam1-20260902/fact-seeking-70shard-10lang-r16-20260903/language=hin_Deva/source=18e67b6d4a372383a93b/chunk=00c5f47ee4e2eeeb507e1059777541f688a22c6b4c4e26f0d062448f5b6dea02/files/hin_Deva/translated_documents.parquet`
- **Column:** `translation`
- **Document id:** `s3://nemotron-training-data-us-east-1/datasets/Nemotron-Pretraining-Specialized-v1.2/Nemotron-Pretraining-Fact-Seeking/part_000009.parquet#rows=7400000:7600000:0` (column `document_id`)
- **Character length:** 192
- **Columns checked:** On this object, `translation` is the translated text (192 characters, not a hex digest). `translation_sha256` is a 64-character hex digest. The sample is `translation`.

```
मरम्मत के बाद, अटलांटिक तट पर प्रशिक्षण के बाद यूएसएस लुडलो किस तारीख को भूमध्य सागर में लौटा?
A. 20 अप्रैल 1943
B. 20 अप्रैल 1942
C. 20 अप्रैल 1945
D. 20 अप्रैल 1944
उत्तरः D. 20 अप्रैल 1944
```


### Fact-Seeking Indic — Bengali

- **S3 key:** `translations/Nemotron-Pretraining-Specialized-v1.2/Fact-Seeking/indictrans2-en-indic-dist-200M-beam1-20260902/fact-seeking-70shard-10lang-r16-20260903/language=ben_Beng/source=24c0607adac25c9e3e90/chunk=02fe47bf5eb2a30701eaa79ea4b79c85625f12d308314d890e9c3cb8a4f36e01/files/ben_Beng/translated_documents.parquet`
- **Column:** `translation`
- **Document id:** `s3://nemotron-training-data-us-east-1/datasets/Nemotron-Pretraining-Specialized-v1.2/Nemotron-Pretraining-Fact-Seeking/part_000007.parquet#rows=4400000:4600000:2` (column `document_id`)
- **Character length:** 312
- **Columns checked:** On this object, `translation` is the translated text (312 characters, not a hex digest). `translation_sha256` is a 64-character hex digest. The sample is `translation`.

```
2022 সালের পুনর্গঠনের পর দ্বিতীয় স্বাস্থ্য ব্যাটালিয়ন কোন সক্ষমতা বৃদ্ধি করেছিল?
A. নৌবাহিনীর চিকিৎসা লজিস্টিক সমন্বয়
B. স্বাস্থ্য ও সংশ্লিষ্ট স্বাস্থ্য সহায়তা বন্ধ করুন
C. বায়ুবাহিত চিকিৎসা মোতায়েনের প্রশিক্ষণ
D. ভূমিকা 3 চিকিৎসা উদ্ধার সহায়তা
উত্তর: B. স্বাস্থ্য ও সংশ্লিষ্ট স্বাস্থ্য সহায়তা বন্ধ করুন
```


### Fact-Seeking Indic — Tamil

- **S3 key:** `translations/Nemotron-Pretraining-Specialized-v1.2/Fact-Seeking/indictrans2-en-indic-dist-200M-beam1-20260902/fact-seeking-70shard-10lang-r16-20260903/language=tam_Taml/source=3cf8b0a24eb61f1314f9/chunk=020c880fb7ea901fdfdf29d68ec0ce7b7588af9a3e1b658462c78388c0e9032b/files/tam_Taml/translated_documents.parquet`
- **Column:** `translation`
- **Document id:** `s3://nemotron-training-data-us-east-1/datasets/Nemotron-Pretraining-Specialized-v1.2/Nemotron-Pretraining-Fact-Seeking/part_000032.parquet#rows=4200000:4400000:0` (column `document_id`)
- **Character length:** 551
- **Columns checked:** On this object, `translation` is the translated text (551 characters, not a hex digest). `translation_sha256` is a 64-character hex digest. The sample is `translation`.

```
1866 ஆம் ஆண்டில், எகிப்தில் சாகுபடி செய்யப்பட்ட வயல்களிலும் ஆற்றுப் பகுதிகளிலும் டெஃப்ரோசியா பர்புரியா கண்டுபிடிக்கப்பட்டதாக ஆவணப்படுத்தப்பட்டது?
A. அசோவானின் கிழக்கு மற்றும் தெற்கே உள்ள பள்ளத்தாக்குகள், எலிஃபென்டைன் தீவுகள், நைல் நதிக்கரையில், எட்ஃபோ மற்றும் ஹெர்மண்டிஸ் ஆகிய இடங்களில் உள்ளன.
B. ஃபாயும் ஒயாஸிஸ் மற்றும் லக்சார்
C. செங்கடல் கடற்கரை மற்றும் ஹுர்காடா
D. நைல் டெல்டா மற்றும் கெய்ரோ
பதில்: A. அசோவானின் கிழக்கு மற்றும் தெற்கே உள்ள பள்ளத்தாக்குகள், எலிஃபென்டைன் தீவுகள், நைல் நதிக்கரையில், எட்ஃபோ மற்றும் ஹெர்மண்டிஸ் ஆகிய இடங்களில் உள்ளன.
```


### Fact-Seeking Indic — Telugu

- **S3 key:** `translations/Nemotron-Pretraining-Specialized-v1.2/Fact-Seeking/indictrans2-en-indic-dist-200M-beam1-20260902/fact-seeking-70shard-10lang-r16-20260903/language=tel_Telu/source=13cbe08f5cd8f06a8aff/chunk=0921f5a7ae2427671110d32dd2a98f18e36b5d304745681ab17ca58c682e259b/files/tel_Telu/translated_documents.parquet`
- **Column:** `translation`
- **Document id:** `s3://nemotron-training-data-us-east-1/datasets/Nemotron-Pretraining-Specialized-v1.2/Nemotron-Pretraining-Fact-Seeking/part_000023.parquet#rows=6600000:6800000:0` (column `document_id`)
- **Character length:** 335
- **Columns checked:** On this object, `translation` is the translated text (335 characters, not a hex digest). `translation_sha256` is a 64-character hex digest. The sample is `translation`.

```
కొలంబియా మరియు మయామి మధ్య ప్రయాణీకుల మార్గాల కోసం ఏఆర్సీఏ దరఖాస్తుకు మద్దతుగా ఏ రేడియో కార్యక్రమం ప్రజా కాల్స్ అందుకుంది?
A. లా డబ్ల్యూ 97.1 ఎఫ్ఎం
B. రేడియో నేషనల్ డి కొలంబియా
C. రేడియో కరాకోల్
D. కొలంబియా లా గ్రాండే, డబ్ల్యుఆర్హెచ్సి ద్వారా ప్రసారం చేయబడింది
సమాధానం: D. కొలంబియా లా గ్రాండే, డబ్ల్యుఆర్హెచ్సి ద్వారా ప్రసారం చేయబడింది
```


### Fact-Seeking Indic — Kannada

- **S3 key:** `translations/Nemotron-Pretraining-Specialized-v1.2/Fact-Seeking/indictrans2-en-indic-dist-200M-beam1-20260902/fact-seeking-70shard-10lang-r16-20260903/language=kan_Knda/source=1f0e85c08c293cf4fda0/chunk=011a9849df3f13375afb192c9b243f578a19ff5412b98f0f8ce4dffd16eb8371/files/kan_Knda/translated_documents.parquet`
- **Column:** `translation`
- **Document id:** `s3://nemotron-training-data-us-east-1/datasets/Nemotron-Pretraining-Specialized-v1.2/Nemotron-Pretraining-Fact-Seeking/part_000030.parquet#rows=3600000:3800000:0` (column `document_id`)
- **Character length:** 479
- **Columns checked:** On this object, `translation` is the translated text (479 characters, not a hex digest). `translation_sha256` is a 64-character hex digest. The sample is `translation`.

```
ಪ್ಯಾಲೇಸ್ ವಾಕ್ ಕಾದಂಬರಿಯಲ್ಲಿ ಆಯಿಶಾ ಮದುವೆಯಾದಾಗ ಯಾವ ಮಹತ್ವದ ಘಟನೆ ನಡೆಯಿತು?
A. ಇದು ಅಲ್-ಸಯ್ಯಿದ್ ಅಹ್ಮದ್ ತನ್ನ ವಿವಾಹೇತರ ಸಂಬಂಧಗಳನ್ನು ಕೊನೆಗೊಳಿಸಲು ಕಾರಣವಾಯಿತು.
B. ಇದು ಫಾಹ್ಮಿಯ ವಿರೋಧದಿಂದಾಗಿ ಕುಟುಂಬದಲ್ಲಿ ರಾಜಕೀಯ ಅಶಾಂತಿಗೆ ನಾಂದಿ ಹಾಡಿತು.
C. ಕುಟುಂಬದಲ್ಲಿ ಮಗಳೊಬ್ಬಳು ಮದುವೆಯಾಗಿರುವುದು ಇದೇ ಮೊದಲು, ಇದು ಖದೀಜಾಳ ಮರೆಮಾಚಲ್ಪಡುವ ಭಯವನ್ನು ಪೂರೈಸಿತು.
D. ಇದು ಕೈರೋದ ಗಮಾಲಿಯಾ ಜಿಲ್ಲೆಯಿಂದ ಕುಟುಂಬವನ್ನು ಸ್ಥಳಾಂತರಿಸಲು ಕಾರಣವಾಯಿತು.
ಉತ್ತರ: C. ಕುಟುಂಬದಲ್ಲಿ ಮಗಳೊಬ್ಬಳು ಮದುವೆಯಾಗಿರುವುದು ಇದೇ ಮೊದಲು, ಇದು ಖದೀಜಾಳ ಮರೆಮಾಚಲ್ಪಡುವ ಭಯವನ್ನು ಪೂರೈಸಿತು.
```


### Fact-Seeking Indic — Marathi

- **S3 key:** `translations/Nemotron-Pretraining-Specialized-v1.2/Fact-Seeking/indictrans2-en-indic-dist-200M-beam1-20260902/fact-seeking-70shard-10lang-r16-20260903/language=mar_Deva/source=2dfe53336872f6321a77/chunk=091742f3c27b640b65b5e32e5e3fc790aa8e3ec22a764177ed8c29e5d542c1e6/files/mar_Deva/translated_documents.parquet`
- **Column:** `translation`
- **Document id:** `s3://nemotron-training-data-us-east-1/datasets/Nemotron-Pretraining-Specialized-v1.2/Nemotron-Pretraining-Fact-Seeking/part_000045.parquet#rows=1000000:1200000:0` (column `document_id`)
- **Character length:** 118
- **Columns checked:** On this object, `translation` is the translated text (118 characters, not a hex digest). `translation_sha256` is a 64-character hex digest. The sample is `translation`.

```
2022 च्या पाकिस्तानी दूरचित्रवाणी मालिका 'मुश्किल' मध्ये हुमायून अश्रफने कोणती भूमिका साकारली होती?
उत्तर: A एस. फॅंड
```


### Fact-Seeking Indic — Gujarati

- **S3 key:** `translations/Nemotron-Pretraining-Specialized-v1.2/Fact-Seeking/indictrans2-en-indic-dist-200M-beam1-20260902/fact-seeking-70shard-10lang-r16-20260903/language=guj_Gujr/source=258d9e4f4da39e095b47/chunk=004da4a4d13107988d822da5edd47544bcc460168e78a65597f91d97a0187e91/files/guj_Gujr/translated_documents.parquet`
- **Column:** `translation`
- **Document id:** `s3://nemotron-training-data-us-east-1/datasets/Nemotron-Pretraining-Specialized-v1.2/Nemotron-Pretraining-Fact-Seeking/part_000060.parquet#rows=7200000:7400000:0` (column `document_id`)
- **Character length:** 216
- **Columns checked:** On this object, `translation` is the translated text (216 characters, not a hex digest). `translation_sha256` is a 64-character hex digest. The sample is `translation`.

```
1995ના બ્રિક્સ્ટન રમખાણો દરમિયાન ભીડને વિખેરવાના તેમના પ્રયાસો અંગે પોલીસે શું જણાવ્યું?
જવાબ: P ઓલીસે જણાવ્યું હતું કે તેમણે પ્રદર્શનકારીઓને શાંતિપૂર્ણ રીતે વિખેરાવાની દરેક તક આપી હતી પરંતુ ટોળાએ તેમ કર્યું ન હતું.
```

