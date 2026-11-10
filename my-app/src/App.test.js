import { render, screen, waitFor } from '@testing-library/react';
import SentimentList from './Components/Sentiment';

beforeEach(() => {
  global.fetch = jest.fn();
});

afterEach(() => {
  jest.restoreAllMocks();
});

test('renders cards from the API', async () => {
  global.fetch.mockResolvedValueOnce({
    ok: true,
    json: async () => [
      {
        location: 'The Mill',
        overall_sentiment: 7,
        maintenance_sentiment: 8,
        distance_sentiment: 6,
        environment_sentiment: 7,
        image_url: '',
        website_url: 'https://www.blacksburgmill.com',
      },
    ],
  });

  render(<SentimentList />);

  await waitFor(() => screen.getByText('The Mill'));

  expect(global.fetch).toHaveBeenCalledWith(
    expect.stringContaining('/sort?by=overall')
  );
});

test('shows an error when the API fails', async () => {
  global.fetch.mockResolvedValueOnce({ ok: false });

  render(<SentimentList />);

  await waitFor(() =>
    expect(screen.getByText(/error/i)).toBeInTheDocument()
  );
});
