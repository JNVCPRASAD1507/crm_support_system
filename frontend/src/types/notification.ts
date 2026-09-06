export interface Notification {
  id: number;
  user_id: number;
  ticket_id: number | null;
  type: string;
  title: string;
  message: string;
  is_read: boolean;
  created_at: string;
}
