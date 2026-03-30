import { API_URL } from './api'

export function connectWorldSocket(worldId, onMessage) {
  const wsUrl = API_URL.replace('http', 'ws') + `/ws/world/${worldId}`
  const socket = new WebSocket(wsUrl)
  socket.onmessage = (event) => onMessage(JSON.parse(event.data))
  return socket
}
