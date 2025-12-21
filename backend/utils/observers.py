"""
Observer Pattern Implementation for Funder Application
This module provides base classes for the Observer pattern.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List


class Subject(ABC):
    """
    Subject (Observable) base class.
    Maintains a list of observers and notifies them of changes.
    """
    
    def __init__(self):
        self._observers: List['Observer'] = []
    
    def attach(self, observer: 'Observer') -> None:
        """Attach an observer to the subject."""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: 'Observer') -> None:
        """Detach an observer from the subject."""
        try:
            self._observers.remove(observer)
        except ValueError:
            pass
    
    def notify(self, event_type: str, data: Dict[str, Any]) -> None:
        """Notify all observers about an event."""
        for observer in self._observers:
            observer.update(event_type, data)


class Observer(ABC):
    """
    Observer base class.
    Defines the interface for objects that should be notified of changes.
    """
    
    @abstractmethod
    def update(self, event_type: str, data: Dict[str, Any]) -> None:
        """
        Receive update from subject.
        
        Args:
            event_type: Type of event that occurred
            data: Event data
        """
        pass


class EventDispatcher:
    """
    Centralized event dispatcher for the application.
    Implements the Observer pattern with event-based notifications.
    """
    
    _instance = None
    _observers: Dict[str, List[Observer]] = {}
    
    def __new__(cls):
        """Singleton pattern - ensure only one dispatcher exists."""
        if cls._instance is None:
            cls._instance = super(EventDispatcher, cls).__new__(cls)
            cls._instance._observers = {}
        return cls._instance
    
    def subscribe(self, event_type: str, observer: Observer) -> None:
        """Subscribe an observer to a specific event type."""
        if event_type not in self._observers:
            self._observers[event_type] = []
        
        if observer not in self._observers[event_type]:
            self._observers[event_type].append(observer)
    
    def unsubscribe(self, event_type: str, observer: Observer) -> None:
        """Unsubscribe an observer from a specific event type."""
        if event_type in self._observers:
            try:
                self._observers[event_type].remove(observer)
            except ValueError:
                pass
    
    def dispatch(self, event_type: str, data: Dict[str, Any]) -> None:
        """Dispatch an event to all subscribed observers."""
        if event_type in self._observers:
            for observer in self._observers[event_type]:
                try:
                    observer.update(event_type, data)
                except Exception as e:
                    # Log error but don't stop other observers
                    print(f"Error notifying observer for {event_type}: {str(e)}")
    
    def clear_all(self) -> None:
        """Clear all observers (useful for testing)."""
        self._observers.clear()
