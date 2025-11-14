# 🌌 Milky Way Dark Matter Visualization

A stunning 3D visualization of the Milky Way galaxy traveling through dark matter and gravitational wave fields, created with React and Three.js.

## ✨ Features

- **3D Milky Way Galaxy**: Spiral galaxy representation with thousands of particles
- **Dark Matter Wave Fields**: Animated wave surfaces representing gravitational pockets
- **Interconnected Particles**: Wave particles that create fluid-like motion
- **Interactive Controls**: Rotate, zoom, and pan to explore the visualization
- **Smooth Animations**: Real-time movement through space with wave effects

## 🚀 Quick Start

### Prerequisites

- Node.js 16+ and npm

### Installation

1. Navigate to the project directory:
```bash
cd milky-way-visualization
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

4. Open [http://localhost:3000](http://localhost:3000) in your browser

## 🎮 Controls

- **Click and Drag**: Rotate the camera around the scene
- **Scroll**: Zoom in and out
- **Right-click and Drag**: Pan the camera

## 🛠️ Technologies

- **React 18**: UI framework
- **@react-three/fiber**: React renderer for Three.js
- **@react-three/drei**: Useful helpers for React Three Fiber
- **Three.js**: 3D graphics library

## 📁 Project Structure

```
milky-way-visualization/
├── src/
│   ├── components/
│   │   └── MilkyWayVisualization.jsx  # Main visualization component
│   ├── App.jsx                         # Main app component
│   ├── App.css                         # Styles
│   ├── index.js                        # Entry point
│   └── index.css                       # Global styles
├── public/
│   └── index.html                      # HTML template
├── package.json                        # Dependencies
└── README.md                           # This file
```

## 🎨 Customization

You can customize the visualization by modifying parameters in `MilkyWayVisualization.jsx`:

- **Galaxy particles**: Change `count` in the `Galaxy` component
- **Wave field resolution**: Adjust `count` in the `WaveField` component
- **Wave particles**: Modify `count` in the `WaveParticles` component
- **Colors**: Adjust color values in the material components
- **Animation speed**: Change `rotationSpeed` and `movementSpeed` values

## 🌟 Features Explained

### Galaxy Component
Creates a spiral galaxy using particle systems with color gradients from warm center to cool edges.

### Wave Field
Animated mesh surface that creates wave patterns using multiple sine wave frequencies for complex, organic motion.

### Wave Particles
Thousands of particles that move in wave patterns, representing dark matter interactions.

### Background Stars
Distant star field for depth and context.

## 📝 License

This project is part of the awesome-generative-ai repository.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

