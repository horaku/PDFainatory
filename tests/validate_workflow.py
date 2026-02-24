import json
from pathlib import Path

wf = json.loads(Path('workflow/n8n-workflow.json').read_text())
node_names = {n['name'] for n in wf['nodes']}
required = {
    'Run PDF Preflight Check',
    'Evaluate Scanned Policy',
    'Scanned Blocked?',
    'Build Fallback Context',
    'Build Fallback Command',
    'Respond Scanned Warning',
}
missing = required - node_names
assert not missing, f"Missing nodes: {sorted(missing)}"

validate = next(n for n in wf['nodes'] if n['name'] == 'Validate & Normalize Input')['parameters']['jsCode']
assert "allowedServices = ['openai', 'google', 'ollama']" in validate
assert 'Unsafe path characters' in validate
assert 'scannedHint' in validate

build = next(n for n in wf['nodes'] if n['name'] == 'Build Translation Command')['parameters']['jsCode']
assert '--bilingual' in build
assert '--auto-enable-ocr-workaround' in build

con = wf['connections']
assert con['Scanned Blocked?']['main'][0][0]['node'] == 'Respond Scanned Warning'
assert con['Scanned Blocked?']['main'][1][0]['node'] == 'Build Corrupt/Encrypted Check'

print('workflow checks passed')
