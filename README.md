
    NOTE: Throughout this documentation the cicada_d core engine will be refered as "theCore"

    The conceptual ideals for cicada_d are fairly basic yet provide versitile scaleability,
    while offering stability at minimal resource cost.
    This is upheld at theCore by adhearing to the following guidelines:

    _events_r0
        1) everything passes through theCore.events_r0 via theCore.__call__
        2) _events_r0 will always have a nested function allowing exosure
            to arguments and returns.
        3) _events_r0 will always return a list to all hooks active in the core as:
            [function, *args, **kwargs]

    theCore / core
        1) Everything initialized in theCore must be editable, controllable, modifiable,
            and removable without breaking theCore. (w/ exceptopn of _events_r0)

        2) All services funcations, variables, exceptiions, decorators, etc,
            that are loaded by theCore, will start and end at theCore, and by theCore.

        3) theCore must never rely on any functions, services, addons, etc; outside of
            INIT to start.

        4) theCore must always start and stop cleanly with 0 loaders.
            However monkey-patching theCore after loading "should be ok"**.
            Example: theCore.logging can be patched as:
                theCore.logging = someservice['newElasticSearch']('random/path/variable')

        5) If theCore doesn't have a specific ability, it will at least provide
            the means to add the ability while maintaing all other guidline points.

    Documentation
        1) LESS IS MORE: don't document the crap out of the source. Offer insight in an occompaning
            txt file or via a "help" or "info" function that points to a doc or url
        2) keep it simple
        4) reuse code, the core is a portable dictionary of functions
        5) replacing functions > being redundant
        6) when in doubt, change it
        7) if it breaks, change it more.
        8) find a crew, find a job, keep flying.

    ** This is a big maybe, might need to provide a plugin system outside of the core to aleviate
        massive debug parties.
        
