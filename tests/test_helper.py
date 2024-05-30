from src.helper import display_message

def test_display_message(mocker):
    mock_log = mocker.patch('src.helper.log.info')
    mock_toast = mocker.patch('src.helper.st.toast')

    message = 'Test message'
    display_message(message, 5)

    mock_log.assert_called_once_with(message)
    mock_toast.assert_called_once_with(message)
