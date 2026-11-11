import { type Media } from '../api/shows'

interface MediaCardProps {
  media: Media
  onAdd?: (id: string) => void
  isAdded?: boolean
}

export default function MediaCard({ media, onAdd, isAdded }: MediaCardProps) {
  return (
    <div className="bg-gray-800 rounded-xl overflow-hidden shadow-lg transition-transform hover:scale-105 flex flex-col">
      {/* Постер */}
      <div className="relative aspect-[2/3] bg-gray-700">
        {media.poster_url ? (
          <img
            src={media.poster_url}
            alt={media.title}
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="flex items-center justify-center h-full text-gray-500 text-sm p-4 text-center">
            Нет постера
          </div>
        )}
        {/* Год в углу постера */}
        <div className="absolute top-2 right-2 bg-black/70 px-2 py-1 rounded text-xs font-bold text-white">
          {media.year || '—'}
        </div>
      </div>
      
      {/* Информация */}
      <div className="p-4 flex flex-col flex-grow">
        <h3 className="text-white font-semibold text-lg line-clamp-2 mb-2" title={media.title}>
          {media.title}
        </h3>
        <div className="mt-auto pt-4">
          {onAdd && (
            <button
              onClick={() => onAdd(media.external_id)}
              disabled={isAdded}
              className={`w-full py-2 rounded-lg text-sm font-medium transition ${
                isAdded
                  ? 'bg-green-600/20 text-green-500 cursor-not-allowed'
                  : 'bg-blue-600 hover:bg-blue-700 text-white'
              }`}
            >
              {isAdded ? 'Уже в списке' : '+ В список'}
            </button>
          )}
        </div>
      </div>
    </div>
  )
}