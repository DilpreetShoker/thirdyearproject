import React from 'react';

const CircularProgressBar = ({ progress, size }) => {
  const radius = size / 2;
  const strokeWidth = 20;
  const normalizedRadius = radius - strokeWidth * 2;
  const circumference = normalizedRadius * 2 * Math.PI;

  const safeProgress = Math.min(100, Math.max(0, Number(progress) || 0));
  
  const strokeDashoffset = circumference - (safeProgress / 100) * circumference;
  

  return (
    <svg height={size} width={size}>
      <circle
        stroke="#093A3E"
        fill="transparent"
        strokeWidth={strokeWidth}
        r={normalizedRadius}
        cx={radius}
        cy={radius}
      />
      <circle
        stroke="white"
        fill="transparent"
        strokeWidth={strokeWidth}
        strokeDasharray={circumference + ' ' + circumference}
        style={{ strokeDashoffset }}
        r={normalizedRadius}
        cx={radius}
        cy={radius}
      />
      <text
        x="50%"
        y="50%"
        textAnchor="middle"
        stroke="#000"
        strokeWidth="1px"
        dy=".3em">
        {`${progress}%`}
      </text>
    </svg>
  );
};

export default CircularProgressBar;