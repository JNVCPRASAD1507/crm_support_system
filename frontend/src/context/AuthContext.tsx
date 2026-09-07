import {
  createContext,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react";

import authService from "../services/authService";

import type {
  LoginRequest,
  Profile,
  RegisterRequest,
} from "../types/auth";

interface AuthContextType {
  user: Profile | null;
  token: string | null;
  loading: boolean;

  login: (data: LoginRequest) => Promise<Profile>;
  register: (data: RegisterRequest) => Promise<Profile>;
  logout: () => void;
  refreshProfile: () => Promise<void>;
}

const AuthContext = createContext<
  AuthContextType | undefined
>(undefined);

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({
  children,
}: AuthProviderProps) {
  const [user, setUser] = useState<Profile | null>(
    null,
  );

  const [token, setToken] = useState<string | null>(
    () => localStorage.getItem("access_token"),
  );

  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const loadUser = async () => {
      const storedToken =
        localStorage.getItem("access_token");

      if (!storedToken) {
        setLoading(false);
        return;
      }

      try {
        const profile =
          await authService.getProfile();

        setUser(profile);
        setToken(storedToken);
      } catch {
        localStorage.removeItem("access_token");
        setUser(null);
        setToken(null);
      } finally {
        setLoading(false);
      }
    };

    loadUser();
  }, []);

  const login = async (
    data: LoginRequest,
  ): Promise<Profile> => {
    const tokenResponse =
      await authService.login(data);

    localStorage.setItem(
      "access_token",
      tokenResponse.access_token,
    );

    setToken(tokenResponse.access_token);

    const profile =
      await authService.getProfile();

    setUser(profile);

    return profile;
  };

  const register = async (
    data: RegisterRequest,
  ): Promise<Profile> => {
    const profile =
      await authService.register(data);

    return profile;
  };

  const logout = () => {
    localStorage.removeItem("access_token");

    setToken(null);
    setUser(null);
  };

  const refreshProfile = async () => {
    const profile =
      await authService.getProfile();

    setUser(profile);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        loading,
        login,
        register,
        logout,
        refreshProfile,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);

  if (!context) {
    throw new Error(
      "useAuth must be used inside AuthProvider",
    );
  }

  return context;
}

