import React, { useContext } from "react";
import commonContext from "../contexts/common/commonContext";
import ErrorPage from "../pages/ErrorPage";

const ProtectedRoute = ({ children }) => {
  const { currentUser, authLoading } = useContext(commonContext);

  if (authLoading) return <div>Loading...</div>;

  if (!currentUser) {
    return <ErrorPage />;
  }

  return children;
};

export default ProtectedRoute;