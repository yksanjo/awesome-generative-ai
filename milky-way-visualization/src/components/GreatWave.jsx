import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { Points, PointMaterial } from '@react-three/drei';
import * as THREE from 'three';

// The Great Wave - A massive ripple traveling across the Milky Way
// Based on: https://www.iflscience.com/there-is-a-great-wave-traveling-across-the-milky-way-shifting-stars-by-100s-of-light-years-80992
// The wave shifts stars vertically by up to 650 light-years and extends 30,000-65,000 light-years horizontally
function GreatWave({ 
  galaxyRadius = 25,
  waveAmplitude = 0.65, // 650 light-years in scaled units (relative to 1000 light-year disk thickness)
  waveLength = 30, // Horizontal extent in scaled units
  waveSpeed = 0.05,
  particleCount = 2000,
  showWave = true,
  position = [0, 0, 0]
}) {
  const groupRef = useRef();
  const particlesRef = useRef();

  const { positions, colors } = useMemo(() => {
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);

    for (let i = 0; i < particleCount; i++) {
      // Distribute particles along the wave region (30,000-65,000 light-years horizontally)
      // In our scaled model, this is roughly 0.6 to 1.3 times galaxy radius
      const angle = Math.random() * Math.PI * 2;
      const radius = (0.6 + Math.random() * 0.7) * galaxyRadius; // Outer disk region
      
      const x = Math.cos(angle) * radius;
      const z = Math.sin(angle) * radius;
      const y = 0; // Will be animated by wave

      positions[i * 3] = x;
      positions[i * 3 + 1] = y;
      positions[i * 3 + 2] = z;

      // Color: stars affected by the wave (reddish for stars above disk, bluish for below)
      const color = new THREE.Color();
      // Mix of colors to show the wave effect
      color.setHSL(0.05 + Math.random() * 0.1, 0.7, 0.5 + Math.random() * 0.3);
      colors[i * 3] = color.r;
      colors[i * 3 + 1] = color.g;
      colors[i * 3 + 2] = color.b;
    }

    return { positions, colors };
  }, [particleCount, galaxyRadius]);

  useFrame((state) => {
    if (particlesRef.current && showWave) {
      const positions = particlesRef.current.geometry.attributes.position.array;
      const time = state.clock.elapsedTime;
      
      // Create a traveling wave effect
      // The wave travels across the galaxy, shifting stars vertically
      for (let i = 0; i < particleCount; i++) {
        const i3 = i * 3;
        const x = positions[i3];
        const z = positions[i3 + 2];
        
        // Calculate distance from center
        const distance = Math.sqrt(x * x + z * z);
        
        // Wave propagates outward/around the galaxy
        // Create a wave pattern that travels
        const wavePhase = (distance / waveLength) - (time * waveSpeed);
        const waveValue = Math.sin(wavePhase * Math.PI * 2) * waveAmplitude;
        
        // Add some angular component to make it spiral-like
        const angle = Math.atan2(z, x);
        const angularWave = Math.sin(angle * 2 + time * waveSpeed * 0.5) * waveAmplitude * 0.3;
        
        // Vertical displacement (the "wave" effect)
        positions[i3 + 1] = waveValue + angularWave;
      }

      particlesRef.current.geometry.attributes.position.needsUpdate = true;
    }
  });

  if (!showWave) return null;

  return (
    <group ref={groupRef} position={position}>
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
    </group>
  );
}

// Visual representation of the wave as a surface
function GreatWaveSurface({
  galaxyRadius = 25,
  waveAmplitude = 0.65,
  waveLength = 30,
  waveSpeed = 0.05,
  segments = 100,
  showSurface = false,
  position = [0, 0, 0]
}) {
  const meshRef = useRef();

  const { positions, normals, indices } = useMemo(() => {
    const positions = [];
    const normals = [];
    const indices = [];

    for (let i = 0; i <= segments; i++) {
      for (let j = 0; j <= segments; j++) {
        const angle = (i / segments) * Math.PI * 2;
        const radius = (0.6 + (j / segments) * 0.7) * galaxyRadius;
        
        const x = Math.cos(angle) * radius;
        const z = Math.sin(angle) * radius;
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
  }, [segments, galaxyRadius]);

  useFrame((state) => {
    if (meshRef.current && meshRef.current.geometry && showSurface) {
      const positions = meshRef.current.geometry.attributes.position.array;
      const time = state.clock.elapsedTime;

      for (let i = 0; i < positions.length; i += 3) {
        const x = positions[i];
        const z = positions[i + 2];
        const distance = Math.sqrt(x * x + z * z);
        
        const wavePhase = (distance / waveLength) - (time * waveSpeed);
        const waveValue = Math.sin(wavePhase * Math.PI * 2) * waveAmplitude;
        
        const angle = Math.atan2(z, x);
        const angularWave = Math.sin(angle * 2 + time * waveSpeed * 0.5) * waveAmplitude * 0.3;
        
        positions[i + 1] = waveValue + angularWave;
      }

      meshRef.current.geometry.attributes.position.needsUpdate = true;
      meshRef.current.geometry.computeVertexNormals();
    }
  });

  if (!showSurface) return null;

  return (
    <mesh ref={meshRef} position={position}>
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
        color="#ff6b6b"
        transparent
        opacity={0.3}
        wireframe={true}
        side={THREE.DoubleSide}
        emissive="#ff4444"
        emissiveIntensity={0.2}
      />
    </mesh>
  );
}

export { GreatWave, GreatWaveSurface };

