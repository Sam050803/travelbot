import Link from "next/link";

export default function HomePage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gradient-to-b from-blue-50 to-white px-4">
      {/* Logo / titre */}
      <div className="text-center mb-8">
        <h1 className="text-5xl font-bold text-gray-800 mb-3">🌍 TravelBot</h1>
        <p className="text-xl text-gray-500 max-w-md">
          Votre assistant touristique personnel, propulsé par l'intelligence artificielle.
        </p>
      </div>

      {/* Carte des fonctionnalités */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-10 max-w-3xl w-full">
        {[
          { icon: "🏨", title: "Hébergements", desc: "Hôtels, locations, conseils budget" },
          { icon: "🍽️", title: "Restaurants", desc: "Gastronomie locale, avis, prix" },
          { icon: "🎭", title: "Activités", desc: "Musées, events, itinéraires" },
        ].map((item) => (
          <div key={item.title} className="bg-white rounded-xl shadow-sm p-5 text-center border border-gray-100">
            <p className="text-3xl mb-2">{item.icon}</p>
            <p className="font-semibold text-gray-800">{item.title}</p>
            <p className="text-sm text-gray-500 mt-1">{item.desc}</p>
          </div>
        ))}
      </div>

      {/* Bouton principal */}
      <Link
        href="/chat"
        className="bg-blue-600 text-white px-8 py-3 rounded-full text-lg font-semibold shadow-md hover:bg-blue-700 transition-colors"
      >
        Démarrer une conversation →
      </Link>
    </div>
  );
}