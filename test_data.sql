-- Insert clients with display_id
INSERT INTO clients (display_id, name, email, phone, source, status, notes, created_at, updated_at) VALUES
('CLIENT-001', 'Alex Johnson', 'alex.johnson@example.com', '+1234567890', 'LinkedIn', 'Second Session Completed', 'Looking to transition from marketing to product management', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('CLIENT-002', 'Jamie Smith', 'jamie.smith@example.com', '+1987654321', 'Website', 'First Session Scheduled', 'Recent graduate looking for career guidance in tech industry', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('CLIENT-003', 'Taylor Davis', 'taylor.davis@example.com', '+1122334455', 'References', 'Info Shared', 'Considering a career change after 10 years in finance', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('CLIENT-004', 'Morgan Lee', 'morgan.lee@example.com', '+1599887766', 'Phone', 'Decision Pending', 'Interested in exploring leadership development options', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
('CLIENT-005', 'Casey Wilson', 'casey.wilson@example.com', '+1443322110', 'LinkedIn', 'Follow-up Scheduled', 'Looking for support with interview preparation', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- For Alex Johnson (Second Session Completed)
INSERT INTO sessions (display_id, client_id, session_number, date, category, completed, notes, zoom_link) VALUES 
('SESSION-001', 1, 1, datetime('now', '-15 days'), 'Initial Consultation', 1, 'Discussed career goals and aspirations. Used Life Design Counselling framework.', 'https://zoom.us/j/abc12345');
INSERT INTO sessions (display_id, client_id, session_number, date, category, completed, notes, zoom_link) VALUES 
('SESSION-002', 1, 2, datetime('now', '-5 days'), 'Initial Consultation', 1, 'Developed actionable goals based on LDC process framework.', 'https://zoom.us/j/def67890');

-- For Jamie Smith (First Session Scheduled)
INSERT INTO sessions (display_id, client_id, session_number, date, category, completed, notes, zoom_link) VALUES
('SESSION-003', 2, 1, datetime('now', '+5 days'), 'Initial Consultation', 0, NULL, 'https://zoom.us/j/ghi23456');

-- For Taylor Davis (Info Shared) - no sessions per your logic

-- For Morgan Lee (Decision Pending) - no sessions per your logic

-- For Casey Wilson (Follow-up Scheduled)
INSERT INTO sessions (display_id, client_id, session_number, date, category, completed, notes, zoom_link) VALUES
('SESSION-004', 5, 1, datetime('now', '-15 days'), 'Initial Consultation', 1, 'Discussed career goals and aspirations. Used Life Design Counselling framework.', 'https://zoom.us/j/mno78901');
INSERT INTO sessions (display_id, client_id, session_number, date, category, completed, notes, zoom_link) VALUES 
('SESSION-005', 5, 2, datetime('now', '-5 days'), 'Initial Consultation', 1, 'Developed actionable goals based on LDC process framework.', 'https://zoom.us/j/pqr23456');
INSERT INTO sessions (display_id, client_id, session_number, date, category, completed, notes, zoom_link) VALUES 
('SESSION-006', 5, 3, datetime('now', '+25 days'), 'Initial Consultation', 0, 'Follow-up session to review progress on goals.', 'https://zoom.us/j/stu56789');

-- For Taylor Davis (Info Shared)
INSERT INTO documents (display_id, client_id, type, content, sent, sent_date, created_at, updated_at) VALUES
('DOCUMENT-001', 3, 'Counselling Objective', 'Initial counselling objectives focusing on career transition and skill development.', 1, datetime('now', '-20 days'), CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- For Morgan Lee (Decision Pending)
INSERT INTO documents (display_id, client_id, type, content, sent, sent_date, created_at, updated_at) VALUES
('DOCUMENT-002', 4, 'Counselling Objective', 'Initial counselling objectives focusing on career transition and skill development.', 1, datetime('now', '-20 days'), CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- For Jamie Smith (First Session Scheduled)
INSERT INTO documents (display_id, client_id, type, content, sent, sent_date, created_at, updated_at) VALUES
('DOCUMENT-003', 2, 'Counselling Objective', 'Initial counselling objectives focusing on career transition and skill development.', 1, datetime('now', '-20 days'), CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- For Alex Johnson (Second Session Completed)
INSERT INTO documents (display_id, client_id, type, content, sent, sent_date, created_at, updated_at) VALUES
('DOCUMENT-004', 1, 'Session Summary', 'Summary of sessions including key insights and action items discussed.', 1, datetime('now', '-3 days'), CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO documents (display_id, client_id, type, content, sent, sent_date, created_at, updated_at) VALUES 
('DOCUMENT-005', 1, 'Counselling Objective', 'Initial counselling objectives focusing on career transition and skill development.', 1, datetime('now', '-20 days'), CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO documents (display_id, client_id, type, content, sent, sent_date, created_at, updated_at) VALUES
('DOCUMENT-006', 1, 'Assessment Details', 'Detailed assessment of strengths, areas for growth, and recommended actions.', 1, datetime('now', '-3 days'), CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

-- For Casey Wilson (Follow-up Scheduled)
INSERT INTO documents (display_id, client_id, type, content, sent, sent_date, created_at, updated_at) VALUES
('DOCUMENT-007', 5, 'Counselling Objective', 'Initial counselling objectives focusing on career transition and skill development.', 1, datetime('now', '-20 days'), CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO documents (display_id, client_id, type, content, sent, sent_date, created_at, updated_at) VALUES
('DOCUMENT-008', 5, 'Session Summary', 'Summary of sessions including key insights and action items discussed.', 1, datetime('now', '-3 days'), CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT INTO documents (display_id, client_id, type, content, sent, sent_date, created_at, updated_at) VALUES
('DOCUMENT-009', 5, 'Assessment Details', 'Detailed assessment of strengths, areas for growth, and recommended actions.', 1, datetime('now', '-3 days'), CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
