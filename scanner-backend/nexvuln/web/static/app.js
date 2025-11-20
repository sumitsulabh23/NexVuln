// NexVuln Web Application JavaScript

const API_BASE = '/api';

// DOM Elements
const targetInput = document.getElementById('target');
const validateBtn = document.getElementById('validateBtn');
const scanBtn = document.getElementById('scanBtn');
const fullScanBtn = document.getElementById('fullScanBtn');
const clearBtn = document.getElementById('clearBtn');
const downloadBtn = document.getElementById('downloadBtn');
const validationResult = document.getElementById('validationResult');
const progressSection = document.getElementById('progressSection');
const resultsSection = document.getElementById('resultsSection');
const progressBar = document.getElementById('progressBar');
const progressText = document.getElementById('progressText');
const scanHeaders = document.getElementById('scanHeaders');
const scanSSL = document.getElementById('scanSSL');
const scanPorts = document.getElementById('scanPorts');
const scanDirectories = document.getElementById('scanDirectories');
const portScanOptions = document.getElementById('portScanOptions');
const portScanType = document.getElementById('portScanType');

let currentResults = {};

// Event Listeners
validateBtn.addEventListener('click', validateTarget);
scanBtn.addEventListener('click', runCustomScan);
fullScanBtn.addEventListener('click', runFullScan);
clearBtn.addEventListener('click', clearResults);
downloadBtn.addEventListener('click', downloadReport);
scanPorts.addEventListener('change', togglePortOptions);

// Toggle port scan options
function togglePortOptions() {
    portScanOptions.style.display = scanPorts.checked ? 'block' : 'none';
}

// Validate Target
async function validateTarget() {
    const target = targetInput.value.trim();
    if (!target) {
        showValidationResult('Please enter a target', 'error');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/validate`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ target })
        });

        const data = await response.json();
        
        if (data.valid) {
            showValidationResult(`✅ Valid target: ${data.host}:${data.port}`, 'success');
        } else {
            showValidationResult(`❌ ${data.error}`, 'error');
        }
    } catch (error) {
        showValidationResult(`❌ Error: ${error.message}`, 'error');
    }
}

function showValidationResult(message, type) {
    validationResult.textContent = message;
    validationResult.className = `validation-result ${type}`;
    setTimeout(() => {
        validationResult.style.display = 'none';
    }, 5000);
}

// Run Custom Scan
async function runCustomScan() {
    const target = targetInput.value.trim();
    if (!target) {
        alert('Please enter a target');
        return;
    }

    currentResults = {
        target: target,
        scan_date: new Date().toISOString(),
        header_scan: [],
        ssl_scan: {},
        port_scan: [],
        directory_scan: []
    };

    showProgress('Initializing scan...', 0);

    const scans = [];
    if (scanHeaders.checked) scans.push(scanHeaderSecurity);
    if (scanSSL.checked) scans.push(scanSSLConfig);
    if (scanPorts.checked) scans.push(scanPortsFunc);
    if (scanDirectories.checked) scans.push(scanDirectoriesFunc);

    if (scans.length === 0) {
        alert('Please select at least one scan option');
        hideProgress();
        return;
    }

    try {
        for (let i = 0; i < scans.length; i++) {
            const progress = ((i + 1) / scans.length) * 100;
            showProgress(`Running scan ${i + 1} of ${scans.length}...`, progress);
            await scans[i]();
        }

        showProgress('Scan complete!', 100);
        setTimeout(() => {
            hideProgress();
            displayResults();
        }, 1000);
    } catch (error) {
        hideProgress();
        alert(`Scan error: ${error.message}`);
    }
}

// Run Full Scan
async function runFullScan() {
    const target = targetInput.value.trim();
    if (!target) {
        alert('Please enter a target');
        return;
    }

    showProgress('Starting full scan...', 0);

    try {
        const response = await fetch(`${API_BASE}/scan/full`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                target,
                scan_type: portScanType.value
            })
        });

        const data = await response.json();

        if (data.success) {
            currentResults = data.results;
            showProgress('Full scan complete!', 100);
            setTimeout(() => {
                hideProgress();
                displayResults();
            }, 1000);
        } else {
            throw new Error(data.error || 'Scan failed');
        }
    } catch (error) {
        hideProgress();
        alert(`Scan error: ${error.message}`);
    }
}

// Individual Scan Functions
async function scanHeaderSecurity() {
    const target = targetInput.value.trim();
    const response = await fetch(`${API_BASE}/scan/headers`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target })
    });
    const data = await response.json();
    if (data.success) {
        currentResults.header_scan = data.results;
    }
}

async function scanSSLConfig() {
    const target = targetInput.value.trim();
    const response = await fetch(`${API_BASE}/scan/ssl`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target })
    });
    const data = await response.json();
    if (data.success) {
        currentResults.ssl_scan = data.results;
    }
}

async function scanPortsFunc() {
    const target = targetInput.value.trim();
    const response = await fetch(`${API_BASE}/scan/ports`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            target,
            scan_type: portScanType.value
        })
    });
    const data = await response.json();
    if (data.success) {
        currentResults.port_scan = data.results;
    }
}

async function scanDirectoriesFunc() {
    const target = targetInput.value.trim();
    const response = await fetch(`${API_BASE}/scan/directories`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ target })
    });
    const data = await response.json();
    if (data.success) {
        currentResults.directory_scan = data.results;
    }
}

// Display Results
function displayResults() {
    resultsSection.style.display = 'block';
    
    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });

    // Display Header Results
    displayHeaderResults();
    
    // Display SSL Results
    displaySSLResults();
    
    // Display Port Results
    displayPortResults();
    
    // Display Directory Results
    displayDirectoryResults();
}

function displayHeaderResults() {
    const panel = document.getElementById('headerResults');
    const results = currentResults.header_scan || [];
    
    if (results.length === 0) {
        panel.innerHTML = '<h3><i class="fas fa-heading"></i> HTTP Security Headers</h3><p class="empty-state">No header scan results</p>';
        return;
    }

    let html = '<h3><i class="fas fa-heading"></i> HTTP Security Headers</h3><table class="result-table"><thead><tr><th>Header</th><th>Status</th><th>Severity</th><th>Value</th></tr></thead><tbody>';
    
    results.forEach(result => {
        const statusBadge = result.present 
            ? '<span class="badge badge-success">✅ Present</span>' 
            : '<span class="badge badge-danger">❌ Missing</span>';
        
        const severityClass = {
            'critical': 'badge-danger',
            'high': 'badge-danger',
            'medium': 'badge-warning',
            'low': 'badge-info',
            'info': 'badge-info'
        }[result.severity] || 'badge-info';
        
        html += `<tr>
            <td><strong>${result.header}</strong></td>
            <td>${statusBadge}</td>
            <td><span class="badge ${severityClass}">${result.severity.toUpperCase()}</span></td>
            <td>${result.value.substring(0, 50)}${result.value.length > 50 ? '...' : ''}</td>
        </tr>`;
    });
    
    html += '</tbody></table>';
    panel.innerHTML = html;
}

function displaySSLResults() {
    const panel = document.getElementById('sslResults');
    const results = currentResults.ssl_scan || {};
    
    if (!results.certificate || Object.keys(results).length === 0) {
        panel.innerHTML = '<h3><i class="fas fa-lock"></i> SSL/TLS Configuration</h3><p class="empty-state">No SSL scan results</p>';
        return;
    }

    let html = '<h3><i class="fas fa-lock"></i> SSL/TLS Configuration</h3>';
    
    // Certificate Info
    if (results.certificate) {
        const cert = results.certificate;
        html += '<h4>Certificate Information</h4><table class="result-table"><tbody>';
        html += `<tr><td><strong>Status</strong></td><td>${cert.valid ? '<span class="badge badge-success">✅ Valid</span>' : '<span class="badge badge-danger">❌ Invalid</span>'}</td></tr>`;
        if (cert.subject) html += `<tr><td><strong>Subject</strong></td><td>${cert.subject}</td></tr>`;
        if (cert.issuer) html += `<tr><td><strong>Issuer</strong></td><td>${cert.issuer}</td></tr>`;
        if (cert.days_until_expiry !== undefined) html += `<tr><td><strong>Days Until Expiry</strong></td><td>${cert.days_until_expiry}</td></tr>`;
        html += '</tbody></table>';
    }
    
    // TLS Versions
    if (results.tls_versions) {
        html += '<h4 style="margin-top: 20px;">TLS Version Support</h4><table class="result-table"><tbody>';
        const versions = ['TLSv1.0', 'TLSv1.1', 'TLSv1.2', 'TLSv1.3'];
        versions.forEach(version => {
            const supported = results.tls_versions.supported?.includes(version);
            const weak = results.tls_versions.weak_versions?.includes(version);
            const status = supported 
                ? (weak ? '<span class="badge badge-warning">⚠️ Supported (WEAK)</span>' : '<span class="badge badge-success">✅ Supported</span>')
                : '<span class="badge badge-secondary">❌ Not Supported</span>';
            html += `<tr><td><strong>${version}</strong></td><td>${status}</td></tr>`;
        });
        html += '</tbody></table>';
    }
    
    // Vulnerabilities
    if (results.vulnerabilities && results.vulnerabilities.length > 0) {
        html += '<h4 style="margin-top: 20px; color: var(--danger-color);">⚠️ Vulnerabilities</h4><table class="result-table"><thead><tr><th>Type</th><th>Severity</th><th>Description</th></tr></thead><tbody>';
        results.vulnerabilities.forEach(vuln => {
            const severityClass = {
                'critical': 'badge-danger',
                'high': 'badge-danger',
                'medium': 'badge-warning',
                'low': 'badge-info'
            }[vuln.severity] || 'badge-info';
            html += `<tr>
                <td><strong>${vuln.type}</strong></td>
                <td><span class="badge ${severityClass}">${vuln.severity.toUpperCase()}</span></td>
                <td>${vuln.description}</td>
            </tr>`;
        });
        html += '</tbody></table>';
    }
    
    panel.innerHTML = html;
}

function displayPortResults() {
    const panel = document.getElementById('portResults');
    const results = currentResults.port_scan || [];
    
    if (results.length === 0) {
        panel.innerHTML = '<h3><i class="fas fa-network-wired"></i> Port Scan</h3><p class="empty-state">No port scan results</p>';
        return;
    }

    let html = '<h3><i class="fas fa-network-wired"></i> Port Scan Results</h3>';
    html += '<table class="result-table"><thead><tr><th>Port</th><th>Protocol</th><th>State</th><th>Service</th><th>Version</th></tr></thead><tbody>';
    
    results.forEach(result => {
        html += `<tr>
            <td><strong>${result.port}</strong></td>
            <td>${result.protocol.toUpperCase()}</td>
            <td><span class="badge badge-success">${result.state.toUpperCase()}</span></td>
            <td>${result.service}</td>
            <td>${result.version || 'N/A'}</td>
        </tr>`;
    });
    
    html += '</tbody></table>';
    panel.innerHTML = html;
}

function displayDirectoryResults() {
    const panel = document.getElementById('directoryResults');
    const results = currentResults.directory_scan || [];
    
    if (results.length === 0) {
        panel.innerHTML = '<h3><i class="fas fa-folder-open"></i> Directory Discovery</h3><p class="empty-state">No directories/files found</p>';
        return;
    }

    let html = '<h3><i class="fas fa-folder-open"></i> Directory Discovery Results</h3>';
    html += '<table class="result-table"><thead><tr><th>Path</th><th>Status Code</th><th>Status</th><th>Size</th></tr></thead><tbody>';
    
    results.forEach(result => {
        const statusBadge = result.status_code === 200 
            ? '<span class="badge badge-success">✅ Found</span>'
            : result.status_code === 403
            ? '<span class="badge badge-warning">🚫 Forbidden</span>'
            : result.status_code === 401
            ? '<span class="badge badge-info">🔒 Unauthorized</span>'
            : result.status_code >= 300 && result.status_code < 400
            ? '<span class="badge badge-info">↪️ Redirect</span>'
            : '<span class="badge badge-info">Found</span>';
        
        html += `<tr>
            <td><strong>${result.path}</strong></td>
            <td>${result.status_code}</td>
            <td>${statusBadge}</td>
            <td>${result.content_length} bytes</td>
        </tr>`;
    });
    
    html += '</tbody></table>';
    panel.innerHTML = html;
}

// Progress Functions
function showProgress(message, percent) {
    progressSection.style.display = 'block';
    progressText.textContent = message;
    progressBar.style.width = `${percent}%`;
    progressBar.textContent = percent > 0 ? `${Math.round(percent)}%` : '';
}

function hideProgress() {
    progressSection.style.display = 'none';
    progressBar.style.width = '0%';
}

// Clear Results
function clearResults() {
    resultsSection.style.display = 'none';
    currentResults = {};
    targetInput.value = '';
    validationResult.style.display = 'none';
}

// Download Report
async function downloadReport() {
    if (!currentResults || Object.keys(currentResults).length === 0) {
        alert('No results to download');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/download`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ results: currentResults })
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `nexvuln_report_${new Date().toISOString().split('T')[0]}.json`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } else {
            throw new Error('Download failed');
        }
    } catch (error) {
        alert(`Download error: ${error.message}`);
    }
}

