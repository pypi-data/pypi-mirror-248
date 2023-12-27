import typing as ty

from injkt import Bind, Config, Injectable, Injktor
from injkt.decorator import inject_attr_deps
from injkt.injkt_lazy import InjktLazy


class IMailService(ty.Protocol):
    def send_mail(self, subject: str, to: str) -> None:
        ...


class SmtpMailService(IMailService):
    def send_mail(self, subject: str, to: str) -> None:
        raise NotImplementedError()


injktor = Injktor(
    Config(
        {
            Bind(IMailService, SmtpMailService, always_reinit=True),
        }
    )
)


@inject_attr_deps
class BusinessLogic(InjktLazy):
    mail_service = Injectable(IMailService)

    def do_business_logic(self) -> None:
        self.mail_service.send_mail("Hello", "world")


BusinessLogic().do_business_logic()
