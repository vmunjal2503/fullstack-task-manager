/**
 * Dashboard — Project overview with stats and recent activity.
 */

export default function Dashboard() {
  const stats = [
    { label: "Total Tasks", value: "47", change: "+5 this week" },
    { label: "In Progress", value: "12", change: "3 overdue" },
    { label: "Completed", value: "28", change: "+8 this week" },
    { label: "Team Members", value: "4", change: "1 pending invite" },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white border-b px-8 py-4">
        <div className="flex items-center justify-between max-w-7xl mx-auto">
          <h1 className="text-xl font-bold text-gray-900">Task Manager</h1>
          <div className="flex items-center gap-4">
            <input
              type="search"
              placeholder="Search tasks..."
              className="px-4 py-2 border rounded-lg text-sm w-64"
            />
            <button className="px-4 py-2 bg-blue-600 text-white rounded-lg text-sm hover:bg-blue-700">
              + New Task
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-8 py-8">
        {/* Stats Grid */}
        <div className="grid grid-cols-4 gap-6 mb-8">
          {stats.map((stat) => (
            <div key={stat.label} className="bg-white rounded-xl p-6 border">
              <p className="text-sm text-gray-500 mb-1">{stat.label}</p>
              <p className="text-3xl font-bold text-gray-900">{stat.value}</p>
              <p className="text-xs text-gray-400 mt-1">{stat.change}</p>
            </div>
          ))}
        </div>

        {/* Projects */}
        <h2 className="text-lg font-semibold mb-4">Projects</h2>
        <div className="grid grid-cols-3 gap-6">
          {[
            { name: "Website Redesign", tasks: 24, progress: 65 },
            { name: "Mobile App v2", tasks: 18, progress: 30 },
            { name: "API Migration", tasks: 5, progress: 90 },
          ].map((project) => (
            <div key={project.name} className="bg-white rounded-xl p-6 border hover:shadow-md transition cursor-pointer">
              <h3 className="font-semibold text-gray-900 mb-2">{project.name}</h3>
              <p className="text-sm text-gray-500 mb-4">{project.tasks} tasks</p>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full transition-all"
                  style={{ width: `${project.progress}%` }}
                />
              </div>
              <p className="text-xs text-gray-400 mt-2">{project.progress}% complete</p>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}
