import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { Points, PointMaterial, Sphere, MeshDistortMaterial } from '@react-three/drei';
import * as THREE from 'three';
import { OrbitalZone, ZoneSeparator, GalacticCenter, SunMarker } from './OrbitalZones';
import { GreatWave, GreatWaveSurface } from './GreatWave';

// Enhanced Galaxy component with more accurate Milky Way structure
function Galaxy({ 
  position, 
  rotationSpeed = 0.2,
  particleCount = 8000,
  galaxyRadius = 25,
  armCount = 4,
  barLength = 8,
  bulgeSize = 3,
  coreGlow = 0.3,
  spiralTightness = 0.5
}) {
  const galaxyRef = useRef();
  const particlesRef = useRef();

  // Generate more accurate Milky Way galaxy particles
  const particles = useMemo(() => {
    const count = particleCount;
    const positions = new Float32Array(count * 3);
    const colors = new Float32Array(count * 3);

    for (let i = 0; i < count; i++) {
      // Create barred spiral structure
      const angle = Math.random() * Math.PI * 2;
      const radius = Math.random() * galaxyRadius;
      
      // Central bulge (dense core)
      let x, y, z;
      if (radius < bulgeSize) {
        // Bulge: spherical distribution
        const phi = Math.acos(2 * Math.random() - 1);
        const theta = Math.random() * Math.PI * 2;
        const r = radius * (0.3 + Math.random() * 0.7);
        x = r * Math.sin(phi) * Math.cos(theta);
        y = r * Math.sin(phi) * Math.sin(theta) * 0.3; // Flattened
        z = r * Math.cos(phi);
      } else {
        // Spiral arms with bar structure
        const normalizedRadius = (radius - bulgeSize) / (galaxyRadius - bulgeSize);
        
        // Bar structure in center
        let barInfluence = 0;
        if (radius < barLength) {
          barInfluence = Math.cos(angle * 2) * (1 - normalizedRadius);
        }
        
        // Spiral arm structure (4 main arms like Milky Way)
        const armIndex = Math.floor((angle / (Math.PI * 2)) * armCount);
        const armAngle = (armIndex / armCount) * Math.PI * 2;
        const spiralAngle = armAngle + Math.log(radius / bulgeSize) * spiralTightness;
        
        // Combine bar and spiral
        const finalAngle = spiralAngle + barInfluence * 0.3;
        
        x = Math.cos(finalAngle) * radius;
        z = Math.sin(finalAngle) * radius;
        y = (Math.random() - 0.5) * 0.4 * (1 - normalizedRadius * 0.5); // Thinner at edges
      }

      // Add some randomness
      x += (Math.random() - 0.5) * 0.3;
      y += (Math.random() - 0.5) * 0.2;
      z += (Math.random() - 0.5) * 0.3;

      positions[i * 3] = x;
      positions[i * 3 + 1] = y;
      positions[i * 3 + 2] = z;

      // More realistic star colors
      const distanceFromCenter = Math.sqrt(x * x + z * z);
      const normalizedDistance = Math.min(distanceFromCenter / galaxyRadius, 1);
      
      // Center: yellow/white (older stars), edges: blue/white (younger stars)
      const color = new THREE.Color();
      if (normalizedDistance < 0.3) {
        // Bulge: yellow/orange (old stars)
        color.setHSL(0.1 + Math.random() * 0.05, 0.7 + Math.random() * 0.2, 0.6 + Math.random() * 0.3);
      } else if (normalizedDistance < 0.6) {
        // Mid: white/yellow
        color.setHSL(0.08 + Math.random() * 0.1, 0.3 + Math.random() * 0.3, 0.7 + Math.random() * 0.2);
      } else {
        // Outer arms: blue/white (young hot stars)
        color.setHSL(0.55 + Math.random() * 0.1, 0.6 + Math.random() * 0.3, 0.5 + Math.random() * 0.3);
      }
      
      colors[i * 3] = color.r;
      colors[i * 3 + 1] = color.g;
      colors[i * 3 + 2] = color.b;

    }

    return { positions, colors };
  }, [particleCount, galaxyRadius, armCount, barLength, bulgeSize, spiralTightness]);

  useFrame((state, delta) => {
    if (galaxyRef.current) {
      galaxyRef.current.rotation.y += rotationSpeed * delta;
    }
  });

  return (
    <group ref={galaxyRef} position={position}>
      <Points 
        ref={particlesRef} 
        positions={particles.positions} 
        colors={particles.colors} 
        stride={3} 
        frustumCulled={false}
      >
        <PointMaterial
          transparent
          vertexColors
          size={0.12}
          sizeAttenuation={true}
          depthWrite={false}
          blending={THREE.AdditiveBlending}
        />
      </Points>
      {/* Central core glow */}
      <Sphere args={[bulgeSize * 0.8, 32, 32]} position={[0, 0, 0]}>
        <MeshDistortMaterial
          color="#ffaa00"
          transparent
          opacity={coreGlow}
          distort={0.3}
          speed={2}
        />
      </Sphere>
    </group>
  );
}

// Wave field representing dark matter/gravitational pockets
function WaveField({ 
  count = 60, 
  waveIntensity = 0.5,
  waveSpeed = 0.5,
  waveColor = "#1a1a3a",
  opacity = 0.6
}) {
  const meshRef = useRef();

  // Create wave geometry
  const { positions, normals, indices } = useMemo(() => {
    const segments = count;
    const positions = [];
    const normals = [];
    const indices = [];

    for (let i = 0; i <= segments; i++) {
      for (let j = 0; j <= segments; j++) {
        const x = (i / segments - 0.5) * 100;
        const z = (j / segments - 0.5) * 100;
        const y = 0;

        positions.push(x, y, z);
        normals.push(0, 1, 0);
      }
    }

    for (let i = 0; i < segments; i++) {
      for (let j = 0; j < segments; j++) {
        const a = i * (segments + 1) + j;
        const b = a + segments + 1;

        indices.push(a, b, a + 1);
        indices.push(b, b + 1, a + 1);
      }
    }

    return {
      positions: new Float32Array(positions),
      normals: new Float32Array(normals),
      indices: new Uint16Array(indices),
    };
  }, [count]);

  useFrame((state) => {
    if (meshRef.current && meshRef.current.geometry) {
      const positions = meshRef.current.geometry.attributes.position.array;
      const time = state.clock.elapsedTime * waveSpeed;

      for (let i = 0; i < positions.length; i += 3) {
        const x = positions[i];
        const z = positions[i + 2];
        
        const wave1 = Math.sin((x * 0.1) + time) * 2;
        const wave2 = Math.sin((z * 0.1) + time * 0.6) * 2;
        const wave3 = Math.sin((x * 0.05 + z * 0.05) + time * 0.8) * 3;
        const wave4 = Math.sin(Math.sqrt(x * x + z * z) * 0.1 - time * 1.2) * 1.5;
        
        positions[i + 1] = (wave1 + wave2 + wave3 + wave4) * waveIntensity;
      }

      meshRef.current.geometry.attributes.position.needsUpdate = true;
      meshRef.current.geometry.computeVertexNormals();
    }
  });

  const color = new THREE.Color(waveColor);

  return (
    <mesh ref={meshRef} rotation={[-Math.PI / 2, 0, 0]} position={[0, -10, 0]}>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={positions.length / 3}
          array={positions}
          itemSize={3}
        />
        <bufferAttribute
          attach="attributes-normal"
          count={normals.length / 3}
          array={normals}
          itemSize={3}
        />
        <bufferAttribute
          attach="index"
          count={indices.length}
          array={indices}
          itemSize={1}
        />
      </bufferGeometry>
      <meshStandardMaterial
        color={color}
        transparent
        opacity={opacity}
        wireframe={false}
        side={THREE.DoubleSide}
        emissive={color}
        emissiveIntensity={0.3}
      />
    </mesh>
  );
}

// Interconnected wave particles with connection lines
function WaveParticles({ 
  count = 2000,
  connectionDistance = 8,
  maxConnections = 500,
  waveIntensity = 5,
  waveSpeed = 0.5,
  particleColor = "#4a4aff",
  connectionOpacity = 0.15
}) {
  const particlesRef = useRef();
  const groupRef = useRef();

  const { positions, colors, connections } = useMemo(() => {
    const positions = new Float32Array(count * 3);
    const colors = new Float32Array(count * 3);
    const particlePositions = [];
    const colorObj = new THREE.Color(particleColor);

    for (let i = 0; i < count; i++) {
      const x = (Math.random() - 0.5) * 100;
      const y = (Math.random() - 0.5) * 30;
      const z = (Math.random() - 0.5) * 100;

      positions[i * 3] = x;
      positions[i * 3 + 1] = y;
      positions[i * 3 + 2] = z;

      particlePositions.push(new THREE.Vector3(x, y, z));

      // Use provided color with variation
      const hue = colorObj.getHSL({}).h;
      const color = new THREE.Color();
      color.setHSL(hue + (Math.random() - 0.5) * 0.1, 0.8, 0.3 + Math.random() * 0.2);
      colors[i * 3] = color.r;
      colors[i * 3 + 1] = color.g;
      colors[i * 3 + 2] = color.b;
    }

    // Create connections between nearby particles
    const connectionLines = [];
    
    for (let i = 0; i < count; i++) {
      for (let j = i + 1; j < count; j++) {
        const distance = particlePositions[i].distanceTo(particlePositions[j]);
        if (distance < connectionDistance) {
          connectionLines.push([i, j]);
          if (connectionLines.length >= maxConnections) break;
        }
      }
      if (connectionLines.length >= maxConnections) break;
    }

    return { positions, colors, connections: connectionLines };
  }, [count, connectionDistance, maxConnections, particleColor]);

  useFrame((state) => {
    if (particlesRef.current) {
      const positions = particlesRef.current.geometry.attributes.position.array;
      const time = state.clock.elapsedTime * waveSpeed;

      for (let i = 0; i < count; i++) {
        const i3 = i * 3;
        const x = positions[i3];
        const z = positions[i3 + 2];

        const wave1 = Math.sin((x * 0.1 + z * 0.1) + time) * waveIntensity;
        const wave2 = Math.sin((x * 0.05 - z * 0.05) + time * 0.6) * (waveIntensity * 0.6);
        const wave3 = Math.sin(Math.sqrt(x * x + z * z) * 0.1 - time * 0.8) * (waveIntensity * 0.4);
        
        positions[i3 + 1] = wave1 + wave2 + wave3;
      }

      particlesRef.current.geometry.attributes.position.needsUpdate = true;
    }
  });

  // Create line geometry for connections
  const lineGeometry = useMemo(() => {
    const linePositions = new Float32Array(connections.length * 6);
    return new THREE.BufferGeometry().setAttribute('position', new THREE.BufferAttribute(linePositions, 3));
  }, [connections.length]);

  const lineRef = useRef();
  const colorObj = new THREE.Color(particleColor);

  useFrame(() => {
    if (particlesRef.current && lineRef.current) {
      const particlePositions = particlesRef.current.geometry.attributes.position.array;
      const linePositions = lineRef.current.geometry.attributes.position.array;

      connections.forEach(([i, j], idx) => {
        const i3 = i * 3;
        const j3 = j * 3;
        const lineIdx = idx * 6;

        linePositions[lineIdx] = particlePositions[i3];
        linePositions[lineIdx + 1] = particlePositions[i3 + 1];
        linePositions[lineIdx + 2] = particlePositions[i3 + 2];

        linePositions[lineIdx + 3] = particlePositions[j3];
        linePositions[lineIdx + 4] = particlePositions[j3 + 1];
        linePositions[lineIdx + 5] = particlePositions[j3 + 2];
      });

      lineRef.current.geometry.attributes.position.needsUpdate = true;
    }
  });

  return (
    <group ref={groupRef}>
      <Points ref={particlesRef} positions={positions} colors={colors} stride={3}>
        <PointMaterial
          transparent
          vertexColors
          size={0.15}
          sizeAttenuation={true}
          depthWrite={false}
          blending={THREE.AdditiveBlending}
        />
      </Points>
      <lineSegments ref={lineRef} geometry={lineGeometry}>
        <lineBasicMaterial color={colorObj} transparent opacity={connectionOpacity} />
      </lineSegments>
    </group>
  );
}

// Background stars
function Stars({ count = 5000, starColor = "#ffffff" }) {
  const starsRef = useRef();
  const colorObj = new THREE.Color(starColor);

  const positions = useMemo(() => {
    const positions = new Float32Array(count * 3);
    for (let i = 0; i < count * 3; i++) {
      positions[i] = (Math.random() - 0.5) * 200;
    }
    return positions;
  }, [count]);

  return (
    <Points ref={starsRef} positions={positions} stride={3} frustumCulled={false}>
      <PointMaterial
        transparent
        color={colorObj}
        size={0.05}
        sizeAttenuation={true}
        depthWrite={false}
      />
    </Points>
  );
}

// Main visualization component
export default function MilkyWayVisualization({ params = {} }) {
  const galaxyPosition = useRef([0, 0, 0]);
  
  const {
    // Galaxy params
    galaxyParticleCount = 8000,
    galaxyRadius = 25,
    galaxyRotationSpeed = 0.2,
    armCount = 4,
    barLength = 8,
    bulgeSize = 3,
    coreGlow = 0.3,
    spiralTightness = 0.5,
    
    // Wave field params
    waveFieldSegments = 60,
    waveIntensity = 0.5,
    waveSpeed = 0.5,
    waveColor = "#1a1a3a",
    waveOpacity = 0.6,
    
    // Wave particles params
    waveParticleCount = 2000,
    connectionDistance = 8,
    maxConnections = 500,
    particleWaveIntensity = 5,
    particleWaveSpeed = 0.5,
    particleColor = "#4a4aff",
    connectionOpacity = 0.15,
    
    // Stars params
    starCount = 5000,
    starColor = "#ffffff",
    
    // Movement params
    movementSpeed = 0.1,
    enableMovement = true,
    
    // Orbital zones params
    showOrbitalZones = true,
    showZoneSeparators = true,
    showGalacticCenter = true,
    showSunMarker = true,
    
    // Great Wave params (from IFLScience article)
    showGreatWave = true,
    greatWaveAmplitude = 0.65, // 650 light-years vertical shift
    greatWaveLength = 30, // Horizontal extent
    greatWaveSpeed = 0.05,
    showGreatWaveSurface = false
  } = params;

  useFrame((state) => {
    if (enableMovement) {
      const time = state.clock.elapsedTime;
      galaxyPosition.current[0] = Math.sin(time * movementSpeed) * 10;
      galaxyPosition.current[2] = time * movementSpeed * 5;
    }
  });

  return (
    <>
      <ambientLight intensity={0.3} />
      <pointLight position={[10, 10, 10]} intensity={0.5} />
      <pointLight position={[-10, -10, -10]} intensity={0.3} color="#4a4aff" />

      <Galaxy 
        position={galaxyPosition.current} 
        rotationSpeed={galaxyRotationSpeed}
        particleCount={galaxyParticleCount}
        galaxyRadius={galaxyRadius}
        armCount={armCount}
        barLength={barLength}
        bulgeSize={bulgeSize}
        coreGlow={coreGlow}
        spiralTightness={spiralTightness}
      />

      {/* Orbital zones and markers */}
      {showGalacticCenter && <GalacticCenter position={galaxyPosition.current} />}
      {showSunMarker && <SunMarker position={galaxyPosition.current} galaxyRadius={galaxyRadius} />}
      
      {showOrbitalZones && (
        <group position={galaxyPosition.current}>
          {/* Red zone - innermost */}
          <OrbitalZone 
            color="#ff4444" 
            minRadius={bulgeSize} 
            maxRadius={galaxyRadius * 0.25} 
            particleCount={150}
            galaxyRadius={galaxyRadius}
            rotationSpeed={galaxyRotationSpeed * 1.5}
            showArrows={true}
          />
          {/* Purple zone */}
          <OrbitalZone 
            color="#aa44ff" 
            minRadius={galaxyRadius * 0.25} 
            maxRadius={galaxyRadius * 0.4} 
            particleCount={150}
            galaxyRadius={galaxyRadius}
            rotationSpeed={galaxyRotationSpeed * 1.2}
            showArrows={true}
          />
          {/* Pink zone */}
          <OrbitalZone 
            color="#ff44aa" 
            minRadius={galaxyRadius * 0.4} 
            maxRadius={galaxyRadius * 0.55} 
            particleCount={150}
            galaxyRadius={galaxyRadius}
            rotationSpeed={galaxyRotationSpeed}
            showArrows={true}
          />
          {/* Green zone - Sun's zone */}
          <OrbitalZone 
            color="#44ff44" 
            minRadius={galaxyRadius * 0.55} 
            maxRadius={galaxyRadius * 0.7} 
            particleCount={150}
            galaxyRadius={galaxyRadius}
            rotationSpeed={galaxyRotationSpeed * 0.9}
            showArrows={true}
          />
          {/* Orange zone */}
          <OrbitalZone 
            color="#ffaa44" 
            minRadius={galaxyRadius * 0.7} 
            maxRadius={galaxyRadius * 0.85} 
            particleCount={150}
            galaxyRadius={galaxyRadius}
            rotationSpeed={galaxyRotationSpeed * 0.8}
            showArrows={true}
          />
          {/* Yellow zone - outermost */}
          <OrbitalZone 
            color="#ffff44" 
            minRadius={galaxyRadius * 0.85} 
            maxRadius={galaxyRadius} 
            particleCount={150}
            galaxyRadius={galaxyRadius}
            rotationSpeed={galaxyRotationSpeed * 0.7}
            showArrows={true}
          />
        </group>
      )}

      {showZoneSeparators && (
        <group position={galaxyPosition.current}>
          <ZoneSeparator radius={galaxyRadius * 0.4} />
          <ZoneSeparator radius={galaxyRadius * 0.55} />
          <ZoneSeparator radius={galaxyRadius * 0.7} />
          <ZoneSeparator radius={galaxyRadius * 0.85} />
        </group>
      )}

      <WaveField 
        count={waveFieldSegments}
        waveIntensity={waveIntensity}
        waveSpeed={waveSpeed}
        waveColor={waveColor}
        opacity={waveOpacity}
      />

      <WaveParticles 
        count={waveParticleCount}
        connectionDistance={connectionDistance}
        maxConnections={maxConnections}
        waveIntensity={particleWaveIntensity}
        waveSpeed={particleWaveSpeed}
        particleColor={particleColor}
        connectionOpacity={connectionOpacity}
      />

      <Stars count={starCount} starColor={starColor} />

      {/* The Great Wave - A massive ripple traveling across the Milky Way */}
      {/* Based on: https://www.iflscience.com/there-is-a-great-wave-traveling-across-the-milky-way-shifting-stars-by-100s-of-light-years-80992 */}
      <GreatWave
        galaxyRadius={galaxyRadius}
        waveAmplitude={greatWaveAmplitude}
        waveLength={greatWaveLength}
        waveSpeed={greatWaveSpeed}
        showWave={showGreatWave}
        position={galaxyPosition.current}
      />
      <GreatWaveSurface
        galaxyRadius={galaxyRadius}
        waveAmplitude={greatWaveAmplitude}
        waveLength={greatWaveLength}
        waveSpeed={greatWaveSpeed}
        showSurface={showGreatWaveSurface}
        position={galaxyPosition.current}
      />
    </>
  );
}
