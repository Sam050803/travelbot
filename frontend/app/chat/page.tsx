import ChatWindow from "../../components/ChatWindow";

export default function ChatPage() {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Header */}
      <header className="bg-blue-600 text-white px-6 py-4 flex items-center gap-3 shadow-sm">
        <span className="text-2xl">🤖</span>
        <div>
          <h1 className="text-lg font-semibold">TravelBot</h1>
          <p className="text-xs text-blue-200">Assistant touristique intelligent</p>
        </div>
      </header>

      {/* Chat — prend tout l'espace restant */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <ChatWindow />
      </div>
    </div>
  );
}