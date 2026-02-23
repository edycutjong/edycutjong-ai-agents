"""License generator — generate open-source license files."""
from __future__ import annotations
from datetime import datetime
from dataclasses import dataclass

LICENSES = {
    "MIT": '''MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.''',
    "Apache-2.0": '''Apache License 2.0

Copyright {year} {author}

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.''',
    "GPL-3.0": '''GNU GENERAL PUBLIC LICENSE Version 3

Copyright (C) {year} {author}

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.''',
    "BSD-3-Clause": '''BSD 3-Clause License

Copyright (c) {year}, {author}
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice.
2. Redistributions in binary form must reproduce the above copyright notice.
3. Neither the name nor the names of its contributors may be used to endorse.''',
    "ISC": '''ISC License

Copyright (c) {year} {author}

Permission to use, copy, modify, and/or distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.''',
    "Unlicense": '''This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute
this software, either in source code form or as a compiled binary, for any
purpose, commercial or non-commercial, and by any means.'''
}

@dataclass
class LicenseResult:
    license_type: str = ""; content: str = ""; author: str = ""; year: int = 0
    def to_dict(self) -> dict: return {"type": self.license_type, "author": self.author, "year": self.year}

def generate(license_type: str, author: str, year: int = None) -> LicenseResult:
    y = year or datetime.now().year
    template = LICENSES.get(license_type, "")
    if not template: return LicenseResult(license_type=license_type, content=f"Unknown license: {license_type}")
    content = template.replace("{year}", str(y)).replace("{author}", author)
    return LicenseResult(license_type=license_type, content=content, author=author, year=y)

def get_available() -> list[str]:
    return list(LICENSES.keys())

def get_summary(license_type: str) -> str:
    summaries = {"MIT": "Permissive, minimal restrictions", "Apache-2.0": "Permissive with patent grant", "GPL-3.0": "Copyleft, source must be shared", "BSD-3-Clause": "Permissive, no endorsement clause", "ISC": "Simplified permissive license", "Unlicense": "Public domain dedication"}
    return summaries.get(license_type, "Unknown license type")

def format_result_markdown(r: LicenseResult) -> str:
    return f"## License Generator 📜\n**Type:** {r.license_type} | **Author:** {r.author} | **Year:** {r.year}"
