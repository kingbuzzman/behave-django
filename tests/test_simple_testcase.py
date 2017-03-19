try:
    import unittest.mock as mock
except ImportError:
    import mock

from .util import DjangoSetupMixin
from behave_django.runner import SimpleTestRunner
from behave.runner import Context, Runner
from django.test.testcases import TestCase
import pytest


class TestSimpleTestCase(DjangoSetupMixin):

    @mock.patch('behave_django.management.commands.behave.behave_main', return_value=0)  # noqa
    @mock.patch('behave_django.management.commands.behave.SimpleTestRunner')  # noqa
    def test_use_simple_test_runner(self,
                                    mock_simple_test_runner,
                                    mock_behave_main):
        self.run_management_command('behave', simple=True)
        mock_behave_main.assert_called_once_with(args=[])
        mock_simple_test_runner.assert_called_once_with()

    def test_simple_test_runner_uses_simple_testcase(self):
        runner = mock.MagicMock()
        context = Context(runner)
        SimpleTestRunner().before_scenario(context)
        assert isinstance(context.test, TestCase)

    def test_simple_testcase_fails_when_accessing_base_url(self):
        runner = Runner(mock.MagicMock())
        runner.context = Context(runner)
        SimpleTestRunner().before_scenario(runner.context)
        with pytest.raises(AssertionError):
            assert runner.context.base_url == 'should raise an exception!'

    def test_simple_testcase_fails_when_calling_get_url(self):
        runner = Runner(mock.MagicMock())
        runner.context = Context(runner)
        SimpleTestRunner().before_scenario(runner.context)
        with pytest.raises(AssertionError):
            runner.context.get_url()