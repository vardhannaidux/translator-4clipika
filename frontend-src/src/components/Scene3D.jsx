import React, { useRef, useState, useEffect } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { Float, MeshDistortMaterial } from '@react-three/drei';

function FloatingPrism() {
  const meshRef = useRef(null);
  const [mouse, setMouse] = useState({ x: 0, y: 0 });

  useEffect(() => {
    const handleMouseMove = (e) => {
      setMouse({
        x: (e.clientX / window.innerWidth) * 2 - 1,
        y: -(e.clientY / window.innerHeight) * 2 + 1,
      });
    };
    window.addEventListener('mousemove', handleMouseMove);
    return () => window.removeEventListener('mousemove', handleMouseMove);
  }, []);

  useFrame((state) => {
    if (!meshRef.current) return;
    const time = state.clock.getElapsedTime();

    // Subtle scroll translation
    const scrollY = window.scrollY;
    meshRef.current.position.y = -scrollY * 0.0025;

    // Follow mouse position slowly (lerping)
    meshRef.current.rotation.x = Math.sin(time * 0.3) * 0.4 + mouse.y * 0.5;
    meshRef.current.rotation.y = time * 0.2 + mouse.x * 0.5;
  });

  return (
    <mesh ref={meshRef} scale={1.8}>
      <octahedronGeometry args={[1, 0]} />
      <MeshDistortMaterial
        color="#3b82f6"
        roughness={0.1}
        metalness={0.1}
        distort={0.3} // Amount of distortion
        speed={1.5}    // Speed of distortion
        clearcoat={1}
        clearcoatRoughness={0.1}
        transmission={0.8} // Glass effect
        thickness={1.5}
      />
    </mesh>
  );
}

export default function Scene3D() {
  const [supportsWebGL, setSupportsWebGL] = useState(true);

  useEffect(() => {
    try {
      const canvas = document.createElement('canvas');
      const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
      if (!gl) setSupportsWebGL(false);
    } catch (e) {
      setSupportsWebGL(false);
    }
  }, []);

  if (!supportsWebGL) {
    return (
      <div className="absolute inset-0 flex items-center justify-center -z-10 opacity-30 select-none pointer-events-none">
        {/* Fallback glow */}
        <div className="w-[300px] h-[300px] rounded-full bg-blue-500/20 blur-[100px] animate-pulse" />
      </div>
    );
  }

  return (
    <div className="absolute inset-0 w-full h-full -z-10 pointer-events-none select-none">
      <Canvas
        camera={{ position: [0, 0, 5], fov: 45 }}
        gl={{ alpha: true, antialias: true }}
      >
        <ambientLight intensity={0.5} />
        <directionalLight position={[5, 10, 5]} intensity={1.5} />
        <pointLight position={[-10, -10, -10]} intensity={1.0} color="#8b5cf6" />
        <Float speed={2} rotationIntensity={1.5} floatIntensity={1.5}>
          <FloatingPrism />
        </Float>
      </Canvas>
    </div>
  );
}
