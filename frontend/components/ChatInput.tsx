"use client";

import { useState } from "react";

interface ChatInputProps {
    onSend: (message: string) => void;
    disabled: boolean;
}

export default function ChatInput({ onSend, disabled }: ChatInputProps) {
    const [input, setInput] = useState("");

    const handleSubmit = () => {
        const trimmed = input.trim();
        if (!trimmed || disabled) return;
        onSend(trimmed);
        setInput("");
    };

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSubmit();
        }
    };

    return (
        <div className="flex gap-2 p-4 border-t border-gray-200 bg-white">
            <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder="Tapez votre message..."
                disabled={disabled}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
            />
            <button
                onClick={handleSubmit}
                disabled={disabled || !input.trim()}

            >
                {disabled ? "Envoi..." : "Envoyer"}
            </button>
        </div>
    );
}