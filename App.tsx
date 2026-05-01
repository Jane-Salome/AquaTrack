import { useState, useEffect } from "react";
import { LandingPage } from "./components/LandingPage";
import { AuthPage } from "./components/AuthPage";
import { Dashboard } from "./components/Dashboard";
import { ReportHazard } from "./components/ReportHazard";
import { AwarenessSection } from "./components/AwarenessSection";
import { AdminPanel } from "./components/AdminPanel";
import { Toaster } from "./components/ui/sonner";

export default function App() {
  const [currentPage, setCurrentPage] = useState("landing");
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [userType, setUserType] = useState("");
  const [userId, setUserId] = useState("");

  const handleNavigation = (page: string) => {
    setCurrentPage(page);
  };

  const handleLogin = (userType: string, userId: string) => {
    setIsLoggedIn(true);
    setUserType(userType);
    setUserId(userId);
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setUserType("");
    setUserId("");
    setCurrentPage("landing");
  };

  // Handle protected page redirects
  useEffect(() => {
    const protectedPages = ["dashboard", "report", "admin"];
    if (!isLoggedIn && protectedPages.includes(currentPage)) {
      setCurrentPage("auth");
    }
  }, [isLoggedIn, currentPage]);

  // Handle admin panel access control
  useEffect(() => {
    if (currentPage === "admin" && userType !== "authority") {
      setCurrentPage("dashboard");
    }
  }, [currentPage, userType]);

  const renderCurrentPage = () => {
    switch (currentPage) {
      case "landing":
        return <LandingPage onNavigate={handleNavigation} />;
      case "auth":
        return (
          <AuthPage
            onNavigate={handleNavigation}
            onLogin={handleLogin}
          />
        );
      case "dashboard":
        return (
          <Dashboard
            onNavigate={handleNavigation}
            userType={userType}
            userId={userId}
            onLogout={handleLogout}
          />
        );
      case "report":
        return <ReportHazard onNavigate={handleNavigation} userId={userId} />;
      case "awareness":
        return (
          <AwarenessSection onNavigate={handleNavigation} />
        );
      case "admin":
        return <AdminPanel onNavigate={handleNavigation} userId={userId} />;
      default:
        return <LandingPage onNavigate={handleNavigation} />;
    }
  };

  return (
    <div className="min-h-screen bg-[var(--background)]">
      {renderCurrentPage()}
      <Toaster />
    </div>
  );
}