document.addEventListener('DOMContentLoaded', function() {
    
document.getElementById('uploadForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById('audio-file');
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    const response = await fetch('/analyze', {
        method: 'POST',
        body: formData
    });

    if (!response.ok) {
        const err = await response.text();
        document.getElementById('result').innerHTML = `<pre>${err}</pre>`;
        return;
    }

    const data = await response.json();
    const features = data.features;
    document.getElementById('result').innerHTML = `
        <pre>${JSON.stringify(data.features, null, 2)}</pre>
    `;

    // Виводимо числові значення
    document.getElementById('result').innerHTML = `
    <table class="audio-features-table">
      <tr><th>Ознака</th><th>Значення</th></tr>
      <tr><td>Темп (BPM)</td><td>${data.features.tempo}</td></tr>
      <tr><td>Середній спектральний центроїд</td><td>${data.features.spectral_centroid.toFixed(2)}</td></tr>
      <tr><td>Zero-Crossing Rate</td><td>${data.features.zero_crossing_rate.toFixed(4)}</td></tr>
      <tr><td>MFCC (середні)</td><td>${data.features.mfcc.map(x => x.toFixed(2)).join(', ')}</td></tr>
      <tr><td>Chroma (середні)</td><td>${data.features.chroma.map(x => x.toFixed(2)).join(', ')}</td></tr>
    </table>
    `;
    // Відображаємо графіки
    document.getElementById('mfccPlot').src = features.plots.mfcc;
    document.getElementById('mfccPlot').style.display = 'block';
    document.getElementById('centroidPlot').src = features.plots.centroid;
    document.getElementById('centroidPlot').style.display = 'block';
    document.getElementById('zcrPlot').src = features.plots.zcr;
    document.getElementById('zcrPlot').style.display = 'block';


    window.analysisFeatures = data.features;
    document.getElementById('findSimilar').style.display = 'inline';
});

document.getElementById('findSimilar').addEventListener('click', async () => {
    const features = window.analysisFeatures;
    const featuresArray = [
        features.tempo,
        features.zero_crossing_rate,        
        features.spectral_centroid,
        ...(features.mfcc || []),
        ...(features.chroma || [])
    ];
    const flatFeatures = featuresArray.flat().filter(x => typeof x === 'number' && !isNaN(x));
    const response = await fetch('/similar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ features: flatFeatures })
    });

    if (!response.ok) {
        const err = await response.text();
        document.getElementById('result').innerHTML = `<pre>${err}</pre>`;
        return;
    }

    const similarTracks = await response.json();
    const list = document.getElementById('similarTracks');
    if (similarTracks.length === 0) {
        list.innerHTML = '<p>Схожих треків не знайдено.</p>';
    } else {
        let html = `
        <table class="audio-features-table">
          <tr><th>Назва треку</th><th>Відстань (distance)</th></tr>
          ${similarTracks.map(track =>
            `<tr>
                <td>${track.title}</td>
                <td>${track.distance.toFixed(4)}</td>
            </tr>`
          ).join('')}
        </table>
        `;
        list.innerHTML = html;
}
    });
});


