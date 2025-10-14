export const APP_CONSTANTS = {
  JWT_EXPIRES_IN: '24h',
  BCRYPT_ROUNDS: 10,
  WEBSOCKET_EVENTS: {
    AUTH: 'auth',
    MAE_UPDATE: 'mae:update',
    FILHO_STATUS: 'filho:status',
    FILHO_SYNC: 'filho:sync',
    FILHO_STATUS_CONFIRMED: 'filho:status:confirmed',
    ERROR: 'error',
  },
  PADROES: {
    PADRAO_1C: '1C',
    PADRAO_1V: '1V',
    PADRAO_NEUTRO: '-',
  },
  STATUS: {
    ON: 'ON',
    OFF: 'OFF',
  },
  USER_TYPES: {
    MAE: 'mae',
    FILHO: 'filho',
  },
} as const;





