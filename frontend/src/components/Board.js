import React from 'react';
import { DragDropContext, Droppable } from 'react-beautiful-dnd';
import List from './List';

function Board({ conversations, setActiveChat }) {
  // Para simplificação, uma lista única "Conversas"
  const convIds = Object.keys(conversations);
  return (
    <div className="board">
      <DragDropContext onDragEnd={() => {}}>
        <Droppable droppableId="conversations">
          {provided => (
            <div className="list" ref={provided.innerRef} {...provided.droppableProps}>
              <h3>Conversas</h3>
              <List convIds={convIds} conversations={conversations} setActiveChat={setActiveChat} />
              {provided.placeholder}
            </div>
          )}
        </Droppable>
      </DragDropContext>
    </div>
  );
}

export default Board;
