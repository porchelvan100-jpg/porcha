import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if GOOGLE_API_KEY:
    client = genai.Client(api_key=GOOGLE_API_KEY)
else:
    client = None


class GeminiDocumentGenerator:

    def __init__(self):
        self.model = "gemini-3.8-flash"

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        dates: str
    ) -> str:

        prompt = f"""
You are a professional legal document drafting assistant.

Generate a clear, structured professional legal document.

Document Type:
{document_type}

Parties Involved:
{parties}

Terms and Conditions:
{terms}

Effective Date:
{dates}

Requirements:
1. Use a professional legal-document structure.
2. Include an appropriate title.
3. Clearly identify all parties.
4. Include the effective date.
5. Include the provided terms and conditions.
6. Add suitable general clauses where appropriate.
7. Use clear section headings.
8. Do not invent specific personal or financial information.
9. End with signature sections.
10. Return only the document content.

This is a generated template and should be reviewed by a qualified legal professional
before being used as a final legal agreement.
"""

        # Try Gemini first
        if client:
            try:
                response = client.models.generate_content(
                    model=self.model,
                    contents=prompt
                )

                if response and response.text:
                    return response.text

            except Exception:
                # Gemini unavailable — use local fallback
                pass

        # Local fallback
        return self._fallback_document(
            document_type,
            parties,
            terms,
            dates
        )

    def _fallback_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        dates: str
    ) -> str:

        return f"""
{document_type.upper()}

EFFECTIVE DATE
{dates}

PARTIES
{parties}

1. PURPOSE

This document sets out the general terms and conditions agreed between
the parties identified above.

2. TERMS AND CONDITIONS

{terms}

3. RESPONSIBILITIES

Each party agrees to perform its responsibilities in accordance with
the terms provided in this document.

4. CONFIDENTIALITY

The parties should keep confidential information received during the
relationship private and should not disclose such information except
where permitted or required by applicable law.

5. TERMINATION

Either party may terminate the agreement in accordance with the
termination terms agreed between the parties.

6. GENERAL PROVISIONS

Any changes to this document should be agreed upon by the parties.
The parties should comply with applicable laws and regulations.

7. SIGNATURES

By signing below, the parties acknowledge that they have reviewed the
terms of this document.

PARTY 1

Name: ______________________________

Signature: _________________________

Date: ______________________________


PARTY 2

Name: ______________________________

Signature: _________________________

Date: ______________________________


DISCLAIMER

This document is an automatically generated template for informational
and drafting purposes. It is not legal advice and should be reviewed
by a qualified legal professional before signing or using it.
""".strip()