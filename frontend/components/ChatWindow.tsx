"use client";

import { useState, useRef, useEffect } from "react";
import MessageBubble from "./MessageBubble";
import ChatInput from "./ChatInput";

// Type pour représenter un message dans notre state local
interface Message {
  id: number;
  content: string;
  isBot: boolean;
  createdAt: string;
}

export default function ChatWindow() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<number | null>(null);
  
  // Référence vers le bas de la liste de messages (pour auto-scroll)
  const messagesEndRef = useRef<HTMLDivElement>(null);
  
  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  // Auto-scroll vers le bas à chaque nouveau message
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Message de bienvenue à l'ouverture
  useEffect(() => {
    setMessages([
      {
        id: 0,
        content: "👋 Bonjour ! Je suis TravelBot, votre assistant touristique. Comment puis-je vous aider aujourd'hui ?",
        isBot: true,
        createdAt: new Date().toISOString()
      }
    ]);
  }, []);

  const sendMessage = async (userMessage: string) => {
    // 1. Ajouter le message utilisateur immédiatement dans l'UI
    const newUserMessage: Message = {
      id: Date.now(),                    // ID temporaire (pas celui de la DB)
      content: userMessage,
      isBot: false,
      createdAt: new Date().toISOString()
    };
    setMessages(prev => [...prev, newUserMessage]);
    setIsLoading(true);

    try {
      // 2. Envoyer la requête au backend
      const response = await fetch(`${API_URL}/api/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          message: userMessage,
          user_id: 1,                    // Pour l'instant, user_id fixe à 1
          conversation_id: conversationId
        })
      });

      if (!response.ok) {
        // En cas d'erreur HTTP, on affiche un message d'erreur
        const errorData = await response.json();
        throw new Error(errorData.detail || "Erreur inconnue");
      }

      // 3. Parser la réponse du backend
      const data = await response.json();

      // 4. Sauvegarder l'ID de conversation (pour les messages suivants)
      if (!conversationId) {
        setConversationId(data.conversation_id);
      }

      // 5. Ajouter la réponse du bot
      const botMessage: Message = {
        id: Date.now() + 1,
        content: data.response,
        isBot: true,
        createdAt: data.timestamp
      };
      setMessages(prev => [...prev, botMessage]);

    } catch (error) {
      // En cas d'erreur, afficher un message d'erreur dans le chat
      const errorMessage: Message = {
        id: Date.now() + 1,
        content: `❌ Oops ! Une erreur s'est produite : ${error instanceof Error ? error.message : "Erreur inconnue"}. Réessayez.`,
        isBot: true,
        createdAt: new Date().toISOString()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Zone des messages — scrollable */}
      <div className="flex-1 overflow-y-auto p-4">
        {messages.map((msg) => (
          <MessageBubble
            key={msg.id}
            content={msg.content}
            isBot={msg.isBot}
            timestamp={msg.createdAt}
          />
        ))}
        
        {/* Indicateur "Le bot réfléchit..." */}
        {isLoading && (
          <div className="flex justify-start mb-3">
            <div className="bg-gray-100 px-4 py-2 rounded-2xl rounded-tl-none shadow-sm">
              <p className="text-gray-500 italic">TravelBot réfléchit...</p>
            </div>
          </div>
        )}
        
        {/* Ancre pour le auto-scroll */}
        <div ref={messagesEndRef} />
      </div>

      {/* Barre d'entrée en bas */}
      <ChatInput onSend={sendMessage} disabled={isLoading} />
    </div>
  );
}