# Quick Start Guide

## Installation & Running

1. **Navigate to the project:**
   ```bash
   cd milky-way-visualization
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm start
   ```

4. **Open your browser:**
   The app will automatically open at [http://localhost:3000](http://localhost:3000)

## What You'll See

- **Milky Way Galaxy**: A beautiful spiral galaxy in the center, rotating slowly
- **Dark Matter Waves**: Animated wave surfaces below the galaxy representing gravitational pockets
- **Interconnected Particles**: Purple/blue particles connected by lines, creating wave-like patterns
- **Background Stars**: Distant stars for depth
- **Smooth Animation**: The galaxy moves through space while waves ripple around it

## Controls

- **Left Click + Drag**: Rotate the camera
- **Scroll Wheel**: Zoom in/out
- **Right Click + Drag**: Pan the camera

## Customization

Edit `src/components/MilkyWayVisualization.jsx` to customize:

- **Galaxy size**: Change particle count in `Galaxy` component
- **Wave intensity**: Adjust wave amplitudes in `WaveField` and `WaveParticles`
- **Colors**: Modify color values in material components
- **Animation speed**: Change `rotationSpeed` and `movementSpeed` values
- **Connection density**: Adjust `maxDistance` in `WaveParticles` component

## Performance Tips

- Reduce particle counts if experiencing lag
- Lower the connection count limit in `WaveParticles` (currently 500)
- Decrease `WaveField` segments count

Enjoy exploring the cosmos! 🌌

