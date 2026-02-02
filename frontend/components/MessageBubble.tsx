interface MessageBubbleProps {
  content: string;
  isBot: boolean;
  timestamp?: string;
}

export default function MessageBubble({ content, isBot, timestamp }: MessageBubbleProps) {
  return (
    <div className={`flex ${isBot ? "justify-start" : "justify-end"} mb-3`}>
      <div className="max-w-[75%]">
        {/* Étiquette : qui a envoyé ? */}
        <p className={`text-xs text-gray-500 mb-1 ${isBot ? "text-left" : "text-right"}`}>
          {isBot ? "🤖 TravelBot" : "Vous"}
        </p>
        
        {/* Bulle de message */}
        <div
          className={`px-4 py-2 rounded-2xl shadow-sm ${
            isBot
              ? "bg-gray-100 text-gray-800 rounded-tl-none"   // Bot : côté gauche, gris
              : "bg-blue-600 text-white rounded-tr-none"       // User : côté droit, bleu
          }`}
        >
          {/* Rendu du texte — on préserve les sauts de ligne du bot */}
          <p className="whitespace-pre-wrap">{content}</p>
        </div>
        
        {/* Horodatage */}
        {timestamp && (
          <p className={`text-xs text-gray-400 mt-1 ${isBot ? "text-left" : "text-right"}`}>
            {new Date(timestamp).toLocaleTimeString("fr-FR", {
              hour: "2-digit",
              minute: "2-digit"
            })}
          </p>
        )}
      </div>
    </div>
  );
}