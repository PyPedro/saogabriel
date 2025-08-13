import React from 'react';
import { Draggable } from 'react-beautiful-dnd';
import Card from './Card';

function List({ convIds, conversations, setActiveChat }) {
  return (
    <div>
      {convIds.map((id, idx) => (
        <Draggable key={id} draggableId={id} index={idx}>
          {provided => (
            <div ref={provided.innerRef} {...provided.draggableProps} {...provided.dragHandleProps}>
              <Card
                title={id}
                preview={conversations[id].lastMessage}
                onClick={() => setActiveChat(id)}
              />
            </div>
          )}
        </Draggable>
      ))}
    </div>
  );
}

export default List;
