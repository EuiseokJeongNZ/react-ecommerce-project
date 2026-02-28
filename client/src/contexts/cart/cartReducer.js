const cartReducer = (state, action) => {
  switch (action.type) {
    case 'ADD_TO_CART': {
      const incoming = action.payload.item;
      const newItemId = incoming.id;

      const normalizedIncoming = {
        ...incoming,
        quantity: Number(incoming.quantity ?? 1),
      };

      const itemExist = state.cartItems.some((item) => item.id === newItemId);

      let updatedCartItems = null;

      if (itemExist) {
        updatedCartItems = state.cartItems.map((item) => {
          if (item.id === newItemId) {
            const currentQty = Number(item.quantity ?? 0);
            return {
              ...item,
              quantity: currentQty + 1,
            };
          }
          return item;
        });
      } else {
        updatedCartItems = [...state.cartItems, normalizedIncoming];
      }

      return {
        ...state,
        cartItems: updatedCartItems,
      };
    }

    case 'REMOVE_FROM_CART':
      return {
        ...state,
        cartItems: state.cartItems.filter((item) => item.id !== action.payload.itemId),
      };

    case 'INCREMENT_ITEM':
      return {
        ...state,
        cartItems: state.cartItems.map((item) => {
          if (item.id === action.payload.itemId) {
            const currentQty = Number(item.quantity ?? 0);
            return {
              ...item,
              quantity: currentQty + 1,
            };
          }
          return item;
        }),
      };

    case 'DECREMENT_ITEM':
      return {
        ...state,
        cartItems: state.cartItems
          .map((item) => {
            if (item.id === action.payload.itemId) {
              const currentQty = Number(item.quantity ?? 0);
              return {
                ...item,
                quantity: currentQty - 1,
              };
            }
            return item;
          })
          .filter((item) => Number(item.quantity) > 0),
      };

    default:
      return state;
  }
};

export default cartReducer;