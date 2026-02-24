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
    'Build Success Audit Record',
    'Build Preflight Audit Record',
    'Build Translation Error Audit Record',
    'Classify Translation Error',
    'Retryable Primary Error?',
    'Increment Primary Retry',
    'Run Translation Retry',
    'Primary Retry Success?',
    'Persist Run State',
    'State Is Success?',
    'State Is Preflight Error?',
    'Validate Output Integrity',
    'Output Integrity Passed?',
    'Publish Artifact Metadata',
    'Build Output Naming Metadata',
    'Build Fidelity Checklist Summary',
    'Build Success Notification',
    'Success Notification Configured?',
    'Send Success Notification',
    'Build Preflight Notification',
    'Preflight Notification Configured?',
    'Send Preflight Notification',
    'Build Translation Notification',
    'Translation Notification Configured?',
    'Send Translation Notification',
}
missing = required - node_names
assert not missing, f"Missing nodes: {sorted(missing)}"

validate = next(n for n in wf['nodes'] if n['name'] == 'Validate & Normalize Input')['parameters']['jsCode']
assert "allowedServices = ['openai', 'google', 'ollama']" in validate
assert 'Unsafe path characters' in validate
assert 'scannedHint' in validate
assert 'inputFileHash' in validate
assert 'runStartedAt' in validate
assert 'artifactBaseUrl' in validate
assert 'artifactStoragePrefix' in validate
assert 'fidelityChecklistMode' in validate
assert 'fidelityWarnMinBytes' in validate
assert 'notificationWebhookUrl' in validate
assert 'notifyOnSuccess' in validate
assert 'notifyOnFailure' in validate
assert 'notifyOnPartial' in validate

classify = next(n for n in wf['nodes'] if n['name'] == 'Classify Translation Error')['parameters']['jsCode']
assert 'translation.transient' in classify
assert 'translation.non_retryable_input' in classify

success_notification = next(n for n in wf['nodes'] if n['name'] == 'Build Success Notification')['parameters']['jsCode']
assert 'success.partial_recovered' in success_notification
assert 'notifyOnPartial' in success_notification
assert 'runOutcomeStatus' in success_notification
assert 'runOutcomeReasonCode' in success_notification

build = next(n for n in wf['nodes'] if n['name'] == 'Build Translation Command')['parameters']['jsCode']
assert '--bilingual' in build
assert '--auto-enable-ocr-workaround' in build

for send_name in ['Send Success Notification', 'Send Preflight Notification', 'Send Translation Notification']:
    send_node = next(n for n in wf['nodes'] if n['name'] == send_name)
    assert send_node['type'] == 'n8n-nodes-base.httpRequest'

con = wf['connections']
assert con['Scanned Blocked?']['main'][0][0]['node'] == 'Respond Scanned Warning'
assert con['Scanned Blocked?']['main'][1][0]['node'] == 'Build Corrupt/Encrypted Check'
assert con['Primary Success?']['main'][0][0]['node'] == 'Build Output Naming Metadata'
assert con['Fallback Success?']['main'][0][0]['node'] == 'Build Output Naming Metadata'
assert con['Primary Retry Success?']['main'][0][0]['node'] == 'Build Output Naming Metadata'
assert con['Build Output Naming Metadata']['main'][0][0]['node'] == 'Validate Output Integrity'
assert con['Output Integrity Passed?']['main'][0][0]['node'] == 'Publish Artifact Metadata'
assert con['Publish Artifact Metadata']['main'][0][0]['node'] == 'Build Fidelity Checklist Summary'
assert con['Build Fidelity Checklist Summary']['main'][0][0]['node'] == 'Build Success Audit Record'
assert con['Output Integrity Passed?']['main'][1][0]['node'] == 'Build Translation Error Audit Record'
assert con['Primary Success?']['main'][1][0]['node'] == 'Classify Translation Error'
assert con['Retryable Primary Error?']['main'][0][0]['node'] == 'Increment Primary Retry'
assert con['Retryable Primary Error?']['main'][1][0]['node'] == 'Build Translation Error Audit Record'
assert con['Primary Retry Success?']['main'][0][0]['node'] == 'Build Output Naming Metadata'
assert con['Primary Retry Success?']['main'][1][0]['node'] == 'Build Fallback Context'
assert con['Fallback Success?']['main'][1][0]['node'] == 'Build Translation Error Audit Record'
assert con['Preflight Passed?']['main'][1][0]['node'] == 'Build Preflight Audit Record'
assert con['Build Success Audit Record']['main'][0][0]['node'] == 'Persist Run State'
assert con['Build Preflight Audit Record']['main'][0][0]['node'] == 'Persist Run State'
assert con['Build Translation Error Audit Record']['main'][0][0]['node'] == 'Persist Run State'
assert con['State Is Success?']['main'][1][0]['node'] == 'State Is Preflight Error?'
assert con['State Is Success?']['main'][0][0]['node'] == 'Build Success Notification'
assert con['Build Success Notification']['main'][0][0]['node'] == 'Success Notification Configured?'
assert con['Success Notification Configured?']['main'][0][0]['node'] == 'Send Success Notification'
assert con['Success Notification Configured?']['main'][1][0]['node'] == 'Respond Success'
assert con['Send Success Notification']['main'][0][0]['node'] == 'Respond Success'
assert con['State Is Preflight Error?']['main'][0][0]['node'] == 'Build Preflight Notification'
assert con['State Is Preflight Error?']['main'][1][0]['node'] == 'Build Translation Notification'
assert con['Build Preflight Notification']['main'][0][0]['node'] == 'Preflight Notification Configured?'
assert con['Preflight Notification Configured?']['main'][0][0]['node'] == 'Send Preflight Notification'
assert con['Preflight Notification Configured?']['main'][1][0]['node'] == 'Respond Preflight Error'
assert con['Send Preflight Notification']['main'][0][0]['node'] == 'Respond Preflight Error'
assert con['Build Translation Notification']['main'][0][0]['node'] == 'Translation Notification Configured?'
assert con['Translation Notification Configured?']['main'][0][0]['node'] == 'Send Translation Notification'
assert con['Translation Notification Configured?']['main'][1][0]['node'] == 'Respond Translation Error'
assert con['Send Translation Notification']['main'][0][0]['node'] == 'Respond Translation Error'

respond_success = next(n for n in wf['nodes'] if n['name'] == 'Respond Success')['parameters']['responseBody']
respond_preflight = next(n for n in wf['nodes'] if n['name'] == 'Respond Preflight Error')['parameters']['responseBody']
respond_translation = next(n for n in wf['nodes'] if n['name'] == 'Respond Translation Error')['parameters']['responseBody']
assert 'audit' in respond_success
assert 'audit' in respond_preflight
assert 'audit' in respond_translation
assert 'retryable' in respond_translation
assert 'retryAttempt' in respond_translation
assert 'errorClass' in respond_translation
assert 'runStateFile' in respond_success
assert 'runStateFile' in respond_preflight
assert 'runStateFile' in respond_translation
assert 'outputFile' in respond_success
assert 'artifact' in respond_success
assert 'outputNaming' in respond_success
assert 'outputFileName' in respond_success
assert 'qualitySummary' in respond_success
assert 'reasonCode' in respond_success
assert 'runOutcomeStatus' in respond_success

print('workflow checks passed')
