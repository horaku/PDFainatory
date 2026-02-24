import json
from pathlib import Path

wf = json.loads(Path('workflow/n8n-workflow.json').read_text())


def node(name: str):
    return next(n for n in wf['nodes'] if n['name'] == name)


def expect_substring(haystack: str, needle: str, context: str):
    if needle not in haystack:
        raise AssertionError(f"Missing '{needle}' in {context}")


validate_code = node('Validate & Normalize Input')['parameters']['jsCode']
build_cmd_code = node('Build Translation Command')['parameters']['jsCode']
fallback_cmd_code = node('Build Fallback Command')['parameters']['jsCode']
respond_success = node('Respond Success')['parameters']['responseBody']

# Payload schema/normalization expectations
for required in [
    'files', 'runId', 'outputDir', 'service', 'poolMaxWorkers',
    'customPromptPath', 'glossaryPath', 'primaryFontFamily',
    'scannedHint', 'allowOcrWorkaround', 'runStateDir',
    'artifactBaseUrl', 'artifactStoragePrefix',
    'fidelityChecklistMode', 'fidelityWarnMinBytes',
    'notificationWebhookUrl', 'notifyOnSuccess', 'notifyOnPartial', 'notifyOnFailure'
]:
    expect_substring(validate_code, required, 'Validate & Normalize Input')

# Command generation contract
for required in ['pdf2zh-next', '--lang-in ja', '--lang-out ru', '--bilingual', '--output', '--pool-max-workers']:
    expect_substring(build_cmd_code, required, 'Build Translation Command')

for required in ['--ignore-cache', '--lang-in ja', '--lang-out ru', '--bilingual']:
    expect_substring(fallback_cmd_code, required, 'Build Fallback Command')

# Success response contract
for required in ['status', 'reasonCode', 'outputNaming', 'qualitySummary', 'artifact', 'runStateFile', 'audit']:
    expect_substring(respond_success, required, 'Respond Success')

print('dry-run checks passed')
