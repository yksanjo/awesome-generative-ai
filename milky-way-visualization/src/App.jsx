import React, { useState } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, PerspectiveCamera } from '@react-three/drei';
import MilkyWayVisualization from './components/MilkyWayVisualization';
import './App.css';

function App() {
  const [showControls, setShowControls] = useState(false);
  
  // Galaxy parameters
  const [galaxyParticleCount, setGalaxyParticleCount] = useState(8000);
  const [galaxyRadius, setGalaxyRadius] = useState(25);
  const [galaxyRotationSpeed, setGalaxyRotationSpeed] = useState(0.2);
  const [armCount, setArmCount] = useState(4);
  const [barLength, setBarLength] = useState(8);
  const [bulgeSize, setBulgeSize] = useState(3);
  const [coreGlow, setCoreGlow] = useState(0.3);
  const [spiralTightness, setSpiralTightness] = useState(0.5);
  
  // Wave field parameters
  const [waveFieldSegments, setWaveFieldSegments] = useState(60);
  const [waveIntensity, setWaveIntensity] = useState(0.5);
  const [waveSpeed, setWaveSpeed] = useState(0.5);
  const [waveOpacity, setWaveOpacity] = useState(0.6);
  
  // Wave particles parameters
  const [waveParticleCount, setWaveParticleCount] = useState(2000);
  const [connectionDistance, setConnectionDistance] = useState(8);
  const [maxConnections, setMaxConnections] = useState(500);
  const [particleWaveIntensity, setParticleWaveIntensity] = useState(5);
  const [particleWaveSpeed, setParticleWaveSpeed] = useState(0.5);
  const [connectionOpacity, setConnectionOpacity] = useState(0.15);
  
  // Other parameters
  const [starCount, setStarCount] = useState(5000);
  const [movementSpeed, setMovementSpeed] = useState(0.1);
  const [enableMovement, setEnableMovement] = useState(true);
  
  // Orbital zones parameters
  const [showOrbitalZones, setShowOrbitalZones] = useState(true);
  const [showZoneSeparators, setShowZoneSeparators] = useState(true);
  const [showGalacticCenter, setShowGalacticCenter] = useState(true);
  const [showSunMarker, setShowSunMarker] = useState(true);
  
  // Great Wave parameters (from IFLScience article)
  const [showGreatWave, setShowGreatWave] = useState(true);
  const [greatWaveAmplitude, setGreatWaveAmplitude] = useState(0.65);
  const [greatWaveLength, setGreatWaveLength] = useState(30);
  const [greatWaveSpeed, setGreatWaveSpeed] = useState(0.05);
  const [showGreatWaveSurface, setShowGreatWaveSurface] = useState(false);

  const params = {
    galaxyParticleCount,
    galaxyRadius,
    galaxyRotationSpeed,
    armCount,
    barLength,
    bulgeSize,
    coreGlow,
    spiralTightness,
    waveFieldSegments,
    waveIntensity,
    waveSpeed,
    waveOpacity,
    waveParticleCount,
    connectionDistance,
    maxConnections,
    particleWaveIntensity,
    particleWaveSpeed,
    connectionOpacity,
    starCount,
    movementSpeed,
    enableMovement,
    showOrbitalZones,
    showZoneSeparators,
    showGalacticCenter,
    showSunMarker,
    showGreatWave,
    greatWaveAmplitude,
    greatWaveLength,
    greatWaveSpeed,
    showGreatWaveSurface
  };

  return (
    <div className="App">
      <div className="canvas-container">
        <Canvas
          gl={{ antialias: true, alpha: true }}
          dpr={[1, 2]}
          style={{ background: 'radial-gradient(circle at center, #0a0a1a 0%, #000000 100%)' }}
        >
          <PerspectiveCamera makeDefault position={[0, 15, 40]} fov={60} />
          <OrbitControls
            enablePan={true}
            enableZoom={true}
            enableRotate={true}
            minDistance={20}
            maxDistance={100}
            autoRotate={false}
            autoRotateSpeed={0.5}
          />
          <MilkyWayVisualization params={params} />
        </Canvas>
      </div>
      
      <div className="info-panel">
        <h1>Milky Way Through Dark Matter</h1>
        <p>
          A 3D visualization of the Milky Way galaxy traveling through 
          dark matter and gravitational wave fields.
        </p>
        <div className="controls-info">
          <p><strong>Controls:</strong></p>
          <ul>
            <li>Click and drag to rotate</li>
            <li>Scroll to zoom</li>
            <li>Right-click and drag to pan</li>
          </ul>
        </div>
        <button 
          className="toggle-controls-btn"
          onClick={() => setShowControls(!showControls)}
        >
          {showControls ? '▼ Hide Parameters' : '▶ Show Parameters'}
        </button>
      </div>

      {showControls && (
        <div className="parameters-panel">
          <h2>Visualization Parameters</h2>
          
          <div className="param-section">
            <h3>🌌 Galaxy</h3>
            <div className="param-group">
              <label>Particle Count: {galaxyParticleCount}</label>
              <input
                type="range"
                min="2000"
                max="15000"
                step="500"
                value={galaxyParticleCount}
                onChange={(e) => setGalaxyParticleCount(Number(e.target.value))}
              />
            </div>
            <div className="param-group">
              <label>Radius: {galaxyRadius}</label>
              <input
                type="range"
                min="10"
                max="50"
                step="1"
                value={galaxyRadius}
                onChange={(e) => setGalaxyRadius(Number(e.target.value))}
              />
            </div>
            <div className="param-group">
              <label>Rotation Speed: {galaxyRotationSpeed.toFixed(2)}</label>
              <input
                type="range"
                min="0"
                max="1"
                step="0.05"
                value={galaxyRotationSpeed}
                onChange={(e) => setGalaxyRotationSpeed(Number(e.target.value))}
              />
            </div>
            <div className="param-group">
              <label>Spiral Arms: {armCount}</label>
              <input
                type="range"
                min="2"
                max="6"
                step="1"
                value={armCount}
                onChange={(e) => setArmCount(Number(e.target.value))}
              />
            </div>
            <div className="param-group">
              <label>Bar Length: {barLength}</label>
              <input
                type="range"
                min="0"
                max="15"
                step="1"
                value={barLength}
                onChange={(e) => setBarLength(Number(e.target.value))}
              />
            </div>
            <div className="param-group">
              <label>Bulge Size: {bulgeSize}</label>
              <input
                type="range"
                min="1"
                max="8"
                step="0.5"
                value={bulgeSize}
                onChange={(e) => setBulgeSize(Number(e.target.value))}
              />
            </div>
            <div className="param-group">
              <label>Core Glow: {coreGlow.toFixed(2)}</label>
              <input
                type="range"
                min="0"
                max="1"
                step="0.05"
                value={coreGlow}
                onChange={(e) => setCoreGlow(Number(e.target.value))}
              />
            </div>
            <div className="param-group">
              <label>Spiral Tightness: {spiralTightness.toFixed(2)}</label>
              <input
                type="range"
                min="0.1"
                max="2"
                step="0.1"
                value={spiralTightness}
                onChange={(e) => setSpiralTightness(Number(e.target.value))}
              />
            </div>
          </div>

          <div className="param-section">
            <h3>🌊 Wave Field</h3>
            <div className="param-group">
              <label>Segments: {waveFieldSegments}</label>
              <input
                type="range"
                min="30"
                max="100"
                step="5"
                value={waveFieldSegments}
                onChange={(e) => setWaveFieldSegments(Number(e.target.value))}
              />
            </div>
            <div className="param-group">
              <label>Wave Intensity: {waveIntensity.toFixed(2)}</label>
              <input
                type="range"
                min="0"
                max="2"
                step="0.1"
                value={waveIntensity}
                onChange={(e) => setWaveIntensity(Number(e.target.value))}
              />
            </div>
            <div className="param-group">
              <label>Wave Speed: {waveSpeed.toFixed(2)}</label>
              <input
                type="range"
                min="0"
                max="2"
                step="0.1"
                value={waveSpeed}
                onChange={(e) => setWaveSpeed(Number(e.target.value))}
              />
            </div>
            <div className="param-group">
              <label>Opacity: {waveOpacity.toFixed(2)}</label>
              <input
                type="range"
                min="0"
                max="1"
                step="0.05"
                value={waveOpacity}
                onChange={(e) => setWaveOpacity(Number(e.target.value))}
              />
            </div>
          </div>

          <div className="param-section">
            <h3>✨ Wave Particles</h3>
            <div className="param-group">
              <label>Particle Count: {waveParticleCount}</label>
              <input
                type="range"
                min="500"
                max="5000"
                step="100"
                value={waveParticleCount}
                onChange={(e) => setWaveParticleCount(Number(e.target.value))}
              />
            </div>
            <div className="param-group">
              <label>Connection Distance: {connectionDistance}</label>
              <input
                type="range"
                min="3"
                max="15"
                step="1"
                value={connectionDistance}
                onChange={(e) => setConnectionDistance(Number(e.target.value))}
              />
            </div>
            <div className="param-group">
              <label>Max Connections: {maxConnections}</label>
              <input
                type="range"
                min="100"
                max="1000"
                step="50"
                value={maxConnections}
                onChange={(e) => setMaxConnections(Number(e.target.value))}
              />
            </div>
            <div className="param-group">
              <label>Wave Intensity: {particleWaveIntensity.toFixed(1)}</label>
              <input
                type="range"
                min="1"
                max="15"
                step="0.5"
                value={particleWaveIntensity}
                onChange={(e) => setParticleWaveIntensity(Number(e.target.value))}
              />
            </div>
            <div className="param-group">
              <label>Wave Speed: {particleWaveSpeed.toFixed(2)}</label>
              <input
                type="range"
                min="0"
                max="2"
                step="0.1"
                value={particleWaveSpeed}
                onChange={(e) => setParticleWaveSpeed(Number(e.target.value))}
              />
            </div>
            <div className="param-group">
              <label>Connection Opacity: {connectionOpacity.toFixed(2)}</label>
              <input
                type="range"
                min="0"
                max="1"
                step="0.05"
                value={connectionOpacity}
                onChange={(e) => setConnectionOpacity(Number(e.target.value))}
              />
            </div>
          </div>

          <div className="param-section">
            <h3>⭐ Other</h3>
            <div className="param-group">
              <label>Star Count: {starCount}</label>
              <input
                type="range"
                min="1000"
                max="10000"
                step="500"
                value={starCount}
                onChange={(e) => setStarCount(Number(e.target.value))}
              />
            </div>
            <div className="param-group">
              <label>Movement Speed: {movementSpeed.toFixed(2)}</label>
              <input
                type="range"
                min="0"
                max="0.5"
                step="0.01"
                value={movementSpeed}
                onChange={(e) => setMovementSpeed(Number(e.target.value))}
              />
            </div>
            <div className="param-group">
              <label>
                <input
                  type="checkbox"
                  checked={enableMovement}
                  onChange={(e) => setEnableMovement(e.target.checked)}
                />
                Enable Galaxy Movement
              </label>
            </div>
          </div>

          <div className="param-section">
            <h3>🌍 Orbital Zones & Markers</h3>
            <div className="param-group">
              <label>
                <input
                  type="checkbox"
                  checked={showOrbitalZones}
                  onChange={(e) => setShowOrbitalZones(e.target.checked)}
                />
                Show Orbital Zones
              </label>
            </div>
            <div className="param-group">
              <label>
                <input
                  type="checkbox"
                  checked={showZoneSeparators}
                  onChange={(e) => setShowZoneSeparators(e.target.checked)}
                />
                Show Zone Separators
              </label>
            </div>
            <div className="param-group">
              <label>
                <input
                  type="checkbox"
                  checked={showGalacticCenter}
                  onChange={(e) => setShowGalacticCenter(e.target.checked)}
                />
                Show Galactic Center (GC)
              </label>
            </div>
            <div className="param-group">
              <label>
                <input
                  type="checkbox"
                  checked={showSunMarker}
                  onChange={(e) => setShowSunMarker(e.target.checked)}
                />
                Show Sun Marker
              </label>
            </div>
          </div>

          <div className="param-section">
            <h3>🌊 The Great Wave</h3>
            <p style={{ fontSize: '11px', color: '#a0a0a0', marginBottom: '10px', fontStyle: 'italic' }}>
              A massive ripple traveling across the Milky Way, shifting stars by up to 650 light-years vertically.
              <br />
              <a href="https://www.iflscience.com/there-is-a-great-wave-traveling-across-the-milky-way-shifting-stars-by-100s-of-light-years-80992" 
                 target="_blank" 
                 rel="noopener noreferrer"
                 style={{ color: '#667eea' }}>
                Learn more
              </a>
            </p>
            <div className="param-group">
              <label>
                <input
                  type="checkbox"
                  checked={showGreatWave}
                  onChange={(e) => setShowGreatWave(e.target.checked)}
                />
                Show Great Wave (Star Displacement)
              </label>
            </div>
            <div className="param-group">
              <label>
                <input
                  type="checkbox"
                  checked={showGreatWaveSurface}
                  onChange={(e) => setShowGreatWaveSurface(e.target.checked)}
                />
                Show Wave Surface (Wireframe)
              </label>
            </div>
            <div className="param-group">
              <label>Wave Amplitude: {greatWaveAmplitude.toFixed(2)}</label>
              <input
                type="range"
                min="0"
                max="2"
                step="0.05"
                value={greatWaveAmplitude}
                onChange={(e) => setGreatWaveAmplitude(Number(e.target.value))}
              />
              <span style={{ fontSize: '11px', color: '#a0a0a0' }}>Vertical shift (650 light-years max)</span>
            </div>
            <div className="param-group">
              <label>Wave Length: {greatWaveLength.toFixed(1)}</label>
              <input
                type="range"
                min="10"
                max="50"
                step="1"
                value={greatWaveLength}
                onChange={(e) => setGreatWaveLength(Number(e.target.value))}
              />
              <span style={{ fontSize: '11px', color: '#a0a0a0' }}>Horizontal extent (30k-65k light-years)</span>
            </div>
            <div className="param-group">
              <label>Wave Speed: {greatWaveSpeed.toFixed(3)}</label>
              <input
                type="range"
                min="0"
                max="0.2"
                step="0.005"
                value={greatWaveSpeed}
                onChange={(e) => setGreatWaveSpeed(Number(e.target.value))}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
