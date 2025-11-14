import React, { useRef, useMemo } from 'react';
import { useFrame } from '@react-three/fiber';
import { Points, PointMaterial, Html, Sphere } from '@react-three/drei';
import * as THREE from 'three';

// Orbital zone particles with directional indicators
function OrbitalZone({ 
  color, 
  minRadius, 
  maxRadius, 
  particleCount = 200,
  galaxyRadius = 25,
  rotationSpeed = 0.2,
  showArrows = true
}) {
  const groupRef = useRef();
  const particlesRef = useRef();
  const arrowsGroupRef = useRef();

  const { positions, colors, arrowData } = useMemo(() => {
    const positions = new Float32Array(particleCount * 3);
    const colors = new Float32Array(particleCount * 3);
    const arrows = [];
    const colorObj = new THREE.Color(color);

    for (let i = 0; i < particleCount; i++) {
      const angle = Math.random() * Math.PI * 2;
      const radius = minRadius + Math.random() * (maxRadius - minRadius);
      
      const x = Math.cos(angle) * radius;
      const z = Math.sin(angle) * radius;
      const y = (Math.random() - 0.5) * 0.2;

      positions[i * 3] = x;
      positions[i * 3 + 1] = y;
      positions[i * 3 + 2] = z;

      colors[i * 3] = colorObj.r;
      colors[i * 3 + 1] = colorObj.g;
      colors[i * 3 + 2] = colorObj.b;

      // Calculate orbital velocity direction (tangential + slight radial component)
      const tangentAngle = angle + Math.PI / 2; // Perpendicular to radius
      const radialComponent = (Math.random() - 0.5) * 0.3; // Some radial motion
      
      arrows.push({
        position: [x, y, z],
        direction: [
          Math.cos(tangentAngle) * (1 - Math.abs(radialComponent)) + Math.cos(angle) * radialComponent,
          0,
          Math.sin(tangentAngle) * (1 - Math.abs(radialComponent)) + Math.sin(angle) * radialComponent
        ]
      });
    }

    return { positions, colors, arrowData: arrows.slice(0, Math.min(50, arrows.length)) };
  }, [particleCount, minRadius, maxRadius, color]);

  // Create arrows
  useMemo(() => {
    if (arrowsGroupRef.current && showArrows) {
      // Clear existing arrows
      while (arrowsGroupRef.current.children.length > 0) {
        arrowsGroupRef.current.remove(arrowsGroupRef.current.children[0]);
      }
      
      // Create new arrows
      arrowData.forEach((arrow) => {
        const dir = new THREE.Vector3(...arrow.direction).normalize();
        const origin = new THREE.Vector3(...arrow.position);
        const arrowHelper = new THREE.ArrowHelper(dir, origin, 1.5, color, 0.3, 0.15);
        arrowsGroupRef.current.add(arrowHelper);
      });
    }
  }, [arrowData, color, showArrows]);

  useFrame((state, delta) => {
    if (groupRef.current) {
      groupRef.current.rotation.y += rotationSpeed * delta;
    }
  });

  return (
    <group ref={groupRef}>
      <Points ref={particlesRef} positions={positions} colors={colors} stride={3}>
        <PointMaterial
          transparent
          vertexColors
          size={0.2}
          sizeAttenuation={true}
          depthWrite={false}
          blending={THREE.AdditiveBlending}
        />
      </Points>
      {showArrows && <group ref={arrowsGroupRef} />}
    </group>
  );
}


// Zone separator lines
function ZoneSeparator({ radius, segments = 64 }) {
  const points = useMemo(() => {
    const curve = new THREE.EllipseCurve(
      0, 0,
      radius, radius,
      0, 2 * Math.PI,
      false,
      0
    );
    const points2D = curve.getPoints(segments);
    return points2D.map(p => new THREE.Vector3(p.x, 0, p.y));
  }, [radius, segments]);

  const positions = useMemo(() => {
    return new Float32Array(points.flatMap(p => [p.x, p.y, p.z]));
  }, [points]);

  return (
    <line>
      <bufferGeometry>
        <bufferAttribute
          attach="attributes-position"
          count={points.length}
          array={positions}
          itemSize={3}
        />
      </bufferGeometry>
      <lineBasicMaterial color="#000000" linewidth={2} />
    </line>
  );
}

// Galactic Center marker
function GalacticCenter({ position = [0, 0, 0] }) {
  return (
    <group position={position}>
      <Sphere args={[0.3, 16, 16]}>
        <meshBasicMaterial color="#000000" />
      </Sphere>
      <Html position={[0, 0.5, 0]} center>
        <div style={{ 
          color: '#ffffff', 
          fontSize: '12px', 
          fontWeight: 'bold',
          textShadow: '0 0 10px rgba(255,255,255,0.8)',
          pointerEvents: 'none'
        }}>
          GC
        </div>
      </Html>
    </group>
  );
}

// Sun's position marker
function SunMarker({ 
  position = [0, 0, 0],
  galaxyRadius = 25 
}) {
  // Sun is about 2/3 from center in one of the spiral arms
  const sunDistance = galaxyRadius * 0.65;
  const sunAngle = Math.PI * 0.3; // Position in a spiral arm
  
  const sunX = Math.cos(sunAngle) * sunDistance;
  const sunZ = Math.sin(sunAngle) * sunDistance;
  
  return (
    <group position={[sunX + position[0], position[1], sunZ + position[2]]}>
      <Sphere args={[0.25, 16, 16]}>
        <meshBasicMaterial color="#ffffff" />
      </Sphere>
      <Sphere args={[0.15, 16, 16]}>
        <meshBasicMaterial color="#000000" />
      </Sphere>
      <Html position={[0, 0.4, 0]} center>
        <div style={{ 
          color: '#ffffff', 
          fontSize: '12px', 
          fontWeight: 'bold',
          textShadow: '0 0 10px rgba(255,255,255,0.8)',
          pointerEvents: 'none'
        }}>
          Sun
        </div>
      </Html>
    </group>
  );
}

export { OrbitalZone, ZoneSeparator, GalacticCenter, SunMarker };

