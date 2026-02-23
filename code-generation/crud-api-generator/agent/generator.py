"""CRUD API generator — scaffold REST API routes from model definitions."""
from __future__ import annotations
import json, re
from dataclasses import dataclass, field

@dataclass
class ModelField:
    name: str
    type: str = "string"  # string, number, boolean, date
    required: bool = True
    unique: bool = False
    default: str = ""

@dataclass
class Model:
    name: str
    fields: list[ModelField] = field(default_factory=list)
    timestamps: bool = True
    def to_dict(self) -> dict:
        return {"name": self.name, "fields": [f.__dict__ for f in self.fields], "timestamps": self.timestamps}

def generate_express_routes(model: Model) -> str:
    n = model.name.lower()
    N = model.name
    lines = [
        f'const express = require("express");',
        f'const router = express.Router();',
        f'',
        f'// In-memory store (replace with database)',
        f'let {n}s = [];',
        f'let nextId = 1;',
        f'',
        f'// GET /{n}s — List all',
        f'router.get("/{n}s", (req, res) => {{',
        f'  res.json({n}s);',
        f'}});',
        f'',
        f'// GET /{n}s/:id — Get by ID',
        f'router.get("/{n}s/:id", (req, res) => {{',
        f'  const item = {n}s.find(i => i.id === parseInt(req.params.id));',
        f'  if (!item) return res.status(404).json({{ error: "{N} not found" }});',
        f'  res.json(item);',
        f'}});',
        f'',
        f'// POST /{n}s — Create',
        f'router.post("/{n}s", (req, res) => {{',
    ]
    required_fields = [f for f in model.fields if f.required]
    if required_fields:
        checks = ", ".join(f'"{f.name}"' for f in required_fields)
        lines.append(f'  const required = [{checks}];')
        lines.append(f'  for (const field of required) {{')
        lines.append(f'    if (!req.body[field]) return res.status(400).json({{ error: `${{field}} is required` }});')
        lines.append(f'  }}')
    lines.extend([
        f'  const item = {{ id: nextId++, ...req.body{", createdAt: new Date().toISOString()" if model.timestamps else ""} }};',
        f'  {n}s.push(item);',
        f'  res.status(201).json(item);',
        f'}});',
        f'',
        f'// PUT /{n}s/:id — Update',
        f'router.put("/{n}s/:id", (req, res) => {{',
        f'  const idx = {n}s.findIndex(i => i.id === parseInt(req.params.id));',
        f'  if (idx === -1) return res.status(404).json({{ error: "{N} not found" }});',
        f'  {n}s[idx] = {{ ...{n}s[idx], ...req.body{", updatedAt: new Date().toISOString()" if model.timestamps else ""} }};',
        f'  res.json({n}s[idx]);',
        f'}});',
        f'',
        f'// DELETE /{n}s/:id — Delete',
        f'router.delete("/{n}s/:id", (req, res) => {{',
        f'  const idx = {n}s.findIndex(i => i.id === parseInt(req.params.id));',
        f'  if (idx === -1) return res.status(404).json({{ error: "{N} not found" }});',
        f'  const deleted = {n}s.splice(idx, 1)[0];',
        f'  res.json(deleted);',
        f'}});',
        f'',
        f'module.exports = router;',
    ])
    return "\n".join(lines)

def generate_fastapi_routes(model: Model) -> str:
    n = model.name.lower()
    N = model.name
    py_types = {"string": "str", "number": "float", "boolean": "bool", "date": "str"}
    lines = [
        f'from fastapi import APIRouter, HTTPException',
        f'from pydantic import BaseModel',
        f'from typing import Optional',
        f'',
        f'router = APIRouter()',
        f'',
        f'class {N}Create(BaseModel):',
    ]
    for fi in model.fields:
        pt = py_types.get(fi.type, "str")
        if fi.required: lines.append(f'    {fi.name}: {pt}')
        else: lines.append(f'    {fi.name}: Optional[{pt}] = None')
    lines.extend([
        f'',
        f'class {N}Response({N}Create):',
        f'    id: int',
    ])
    if model.timestamps:
        lines.append(f'    created_at: Optional[str] = None')
    lines.extend([
        f'',
        f'{n}s: list[dict] = []',
        f'next_id = 1',
        f'',
        f'@router.get("/{n}s")',
        f'def list_{n}s():',
        f'    return {n}s',
        f'',
        f'@router.get("/{n}s/{{item_id}}")',
        f'def get_{n}(item_id: int):',
        f'    item = next((i for i in {n}s if i["id"] == item_id), None)',
        f'    if not item: raise HTTPException(404, "{N} not found")',
        f'    return item',
        f'',
        f'@router.post("/{n}s", status_code=201)',
        f'def create_{n}(data: {N}Create):',
        f'    global next_id',
        f'    item = {{"id": next_id, **data.dict()}}',
        f'    next_id += 1',
        f'    {n}s.append(item)',
        f'    return item',
        f'',
        f'@router.delete("/{n}s/{{item_id}}")',
        f'def delete_{n}(item_id: int):',
        f'    global {n}s',
        f'    item = next((i for i in {n}s if i["id"] == item_id), None)',
        f'    if not item: raise HTTPException(404, "{N} not found")',
        f'    {n}s = [i for i in {n}s if i["id"] != item_id]',
        f'    return item',
    ])
    return "\n".join(lines)

def parse_model_definition(definition: str) -> Model:
    """Parse a simple model definition string like 'User: name:string, email:string:required'."""
    parts = definition.split(":")
    if len(parts) < 2: return Model(name=definition.strip())
    name = parts[0].strip()
    fields_str = ":".join(parts[1:]).strip()
    fields = []
    for fdef in fields_str.split(","):
        fdef = fdef.strip()
        if not fdef: continue
        fparts = fdef.split(":")
        fname = fparts[0].strip()
        ftype = fparts[1].strip() if len(fparts) > 1 else "string"
        freq = "required" in fdef
        fields.append(ModelField(name=fname, type=ftype, required=freq))
    return Model(name=name, fields=fields)

def list_endpoints(model: Model) -> list[dict]:
    n = model.name.lower()
    return [
        {"method": "GET", "path": f"/{n}s", "description": f"List all {n}s"},
        {"method": "GET", "path": f"/{n}s/:id", "description": f"Get {n} by ID"},
        {"method": "POST", "path": f"/{n}s", "description": f"Create new {n}"},
        {"method": "PUT", "path": f"/{n}s/:id", "description": f"Update {n}"},
        {"method": "DELETE", "path": f"/{n}s/:id", "description": f"Delete {n}"},
    ]
