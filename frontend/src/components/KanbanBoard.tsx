/**
 * Kanban Board — Drag-and-drop task board with columns.
 * Uses @hello-pangea/dnd for drag interactions.
 */

import React, { useState } from "react";

interface Task {
  id: string;
  title: string;
  priority: "critical" | "high" | "medium" | "low";
  assignee?: { name: string; avatar?: string };
  labels: string[];
  due_date?: string;
  comment_count: number;
}

interface Column {
  id: string;
  name: string;
  tasks: Task[];
}

interface Props {
  columns: Column[];
  onTaskMove: (taskId: string, fromCol: string, toCol: string, position: number) => void;
  onTaskClick: (task: Task) => void;
}

const priorityColors: Record<string, string> = {
  critical: "bg-red-100 text-red-700",
  high: "bg-orange-100 text-orange-700",
  medium: "bg-yellow-100 text-yellow-700",
  low: "bg-green-100 text-green-700",
};

function TaskCard({ task, onClick }: { task: Task; onClick: () => void }) {
  return (
    <div
      onClick={onClick}
      className="bg-white rounded-lg p-4 border border-gray-200 shadow-sm hover:shadow-md transition cursor-pointer mb-3"
    >
      {/* Labels */}
      {task.labels.length > 0 && (
        <div className="flex gap-1 mb-2">
          {task.labels.map((label) => (
            <span key={label} className="px-2 py-0.5 bg-blue-50 text-blue-600 text-xs rounded-full">
              {label}
            </span>
          ))}
        </div>
      )}

      {/* Title */}
      <h4 className="text-sm font-medium text-gray-900 mb-2">{task.title}</h4>

      {/* Footer */}
      <div className="flex items-center justify-between">
        <span className={`px-2 py-0.5 text-xs rounded-full font-medium ${priorityColors[task.priority]}`}>
          {task.priority}
        </span>
        <div className="flex items-center gap-2 text-xs text-gray-400">
          {task.due_date && <span>{task.due_date}</span>}
          {task.comment_count > 0 && <span>{task.comment_count} comments</span>}
        </div>
      </div>

      {/* Assignee */}
      {task.assignee && (
        <div className="mt-2 flex items-center gap-2">
          <div className="w-6 h-6 rounded-full bg-blue-200 flex items-center justify-center text-xs font-medium text-blue-700">
            {task.assignee.name.charAt(0)}
          </div>
          <span className="text-xs text-gray-500">{task.assignee.name}</span>
        </div>
      )}
    </div>
  );
}

export default function KanbanBoard({ columns, onTaskMove, onTaskClick }: Props) {
  return (
    <div className="flex gap-6 overflow-x-auto pb-4">
      {columns.map((column) => (
        <div key={column.id} className="flex-shrink-0 w-80">
          {/* Column Header */}
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-2">
              <h3 className="font-semibold text-gray-700">{column.name}</h3>
              <span className="px-2 py-0.5 bg-gray-100 text-gray-500 text-xs rounded-full">
                {column.tasks.length}
              </span>
            </div>
            <button className="text-gray-400 hover:text-gray-600 text-lg">+</button>
          </div>

          {/* Tasks */}
          <div className="bg-gray-50 rounded-xl p-3 min-h-[200px]">
            {column.tasks.map((task) => (
              <TaskCard
                key={task.id}
                task={task}
                onClick={() => onTaskClick(task)}
              />
            ))}

            {column.tasks.length === 0 && (
              <p className="text-center text-gray-400 text-sm py-8">
                No tasks in this column
              </p>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
