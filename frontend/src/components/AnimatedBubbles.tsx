import React from 'react';
import { Box, keyframes } from '@mui/material';

const float = keyframes`
  0% {
    transform: translateY(100vh) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 1;
  }
  90% {
    opacity: 1;
  }
  100% {
    transform: translateY(-100vh) rotate(360deg);
    opacity: 0;
  }
`;

const floatLeft = keyframes`
  0% {
    transform: translateY(100vh) translateX(-50px) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 0.8;
  }
  90% {
    opacity: 0.8;
  }
  100% {
    transform: translateY(-100vh) translateX(50px) rotate(360deg);
    opacity: 0;
  }
`;

const floatRight = keyframes`
  0% {
    transform: translateY(100vh) translateX(50px) rotate(0deg);
    opacity: 0;
  }
  10% {
    opacity: 0.6;
  }
  90% {
    opacity: 0.6;
  }
  100% {
    transform: translateY(-100vh) translateX(-50px) rotate(-360deg);
    opacity: 0;
  }
`;

const getBubbleStyle = (color: string) => ({
  position: 'absolute',
  borderRadius: '50%',
  background: `linear-gradient(135deg, ${color}, ${color.replace('0.', '0.0')})`,
  border: `1px solid ${color.replace(/[\d.]+\)$/, '0.4)')}`,
  backdropFilter: 'blur(6px)',
  boxShadow: `0 8px 32px ${color}`,
  pointerEvents: 'none',
  zIndex: 0,
});

const AnimatedBubbles: React.FC = () => {
  const bubbles = [
    { size: 60, left: '10%', duration: 15, delay: 0, animation: float, color: 'rgba(25, 118, 210, 0.2)' }, // Primary blue
    { size: 80, left: '20%', duration: 18, delay: 2, animation: floatLeft, color: 'rgba(33, 150, 243, 0.15)' }, // Light blue
    { size: 40, left: '35%', duration: 12, delay: 4, animation: float, color: 'rgba(13, 71, 161, 0.18)' }, // Dark blue
    { size: 100, left: '50%', duration: 20, delay: 1, animation: floatRight, color: 'rgba(63, 81, 181, 0.12)' }, // Indigo blue
    { size: 30, left: '65%', duration: 14, delay: 3, animation: float, color: 'rgba(30, 136, 229, 0.16)' }, // Material blue
    { size: 70, left: '75%', duration: 16, delay: 5, animation: floatLeft, color: 'rgba(21, 101, 192, 0.14)' }, // Deep blue
    { size: 50, left: '85%', duration: 13, delay: 2.5, animation: floatRight, color: 'rgba(68, 138, 255, 0.13)' }, // Bright blue
    { size: 90, left: '5%', duration: 17, delay: 4.5, animation: float, color: 'rgba(41, 121, 255, 0.11)' }, // Vibrant blue
    { size: 35, left: '25%', duration: 11, delay: 6, animation: floatLeft, color: 'rgba(25, 118, 210, 0.17)' }, // Primary blue variant
    { size: 65, left: '45%', duration: 19, delay: 1.5, animation: floatRight, color: 'rgba(57, 73, 171, 0.15)' }, // Navy blue
    { size: 45, left: '60%', duration: 15, delay: 3.5, animation: float, color: 'rgba(92, 107, 192, 0.14)' }, // Soft blue
    { size: 85, left: '80%', duration: 14, delay: 0.5, animation: floatLeft, color: 'rgba(48, 79, 254, 0.12)' }, // Electric blue
  ];

  return (
    <Box
      sx={{
        position: 'fixed',
        top: 0,
        left: 0,
        width: '100vw',
        height: '100vh',
        overflow: 'hidden',
        zIndex: 0,
        pointerEvents: 'none',
      }}
    >
      {bubbles.map((bubble, index) => (
        <Box
          key={index}
          sx={{
            ...getBubbleStyle(bubble.color),
            width: bubble.size,
            height: bubble.size,
            left: bubble.left,
            animation: `${bubble.animation} ${bubble.duration}s linear ${bubble.delay}s infinite`,
          }}
        />
      ))}
    </Box>
  );
};

export default AnimatedBubbles;