import React from 'react';

function Card({ title, preview, onClick }) {
  return (
    <div className="card" onClick={onClick}>
      <div className="card-title">{title}</div>
      <div className="card-preview">{preview}</div>
    </div>
  );
}

export default Card;
