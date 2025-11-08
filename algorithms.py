from collections import deque, OrderedDict

def simulate_fifo(refs, frame_count):
    frames = [-1] * frame_count
    queue = deque()
    timeline = []
    faults = 0
    for ref in refs:
        hit = ref in frames
        evicted = None
        if not hit:
            faults += 1
            if -1 in frames:
                frames[frames.index(-1)] = ref
                queue.append(ref)
            else:
                to_evict = queue.popleft()
                evicted = to_evict
                frames[frames.index(to_evict)] = ref
                queue.append(ref)
        timeline.append({'ref': ref, 'frames': frames.copy(), 'hit': hit, 'evicted': evicted})
    hits = len(refs) - faults
    return timeline, {'faults': faults, 'hits': hits, 'hit_ratio': hits/len(refs) if refs else 0}

def simulate_lru(refs, frame_count):
    frames = []
    recent = OrderedDict()
    timeline = []
    faults = 0
    for ref in refs:
        hit = ref in frames
        evicted = None
        if hit:
            # move to end to mark as recently used
            if ref in recent:
                recent.move_to_end(ref)
        else:
            faults += 1
            if len(frames) < frame_count:
                frames.append(ref)
            else:
                # least recently used is first key in OrderedDict
                if recent:
                    lru = next(iter(recent))
                    evicted = lru
                    frames[frames.index(lru)] = ref
                    recent.pop(lru, None)
            recent[ref] = True
        timeline.append({'ref': ref, 'frames': frames.copy(), 'hit': hit, 'evicted': evicted})
    hits = len(refs) - faults
    return timeline, {'faults': faults, 'hits': hits, 'hit_ratio': hits/len(refs) if refs else 0}

def simulate_optimal(refs, frame_count):
    frames = []
    timeline = []
    faults = 0
    n = len(refs)
    for i, ref in enumerate(refs):
        hit = ref in frames
        evicted = None
        if not hit:
            faults += 1
            if len(frames) < frame_count:
                frames.append(ref)
            else:
                # compute next usage distance for each page in frames
                next_use = {}
                for p in frames:
                    try:
                        j = refs.index(p, i+1)
                        next_use[p] = j
                    except ValueError:
                        next_use[p] = float('inf')
                # evict the page with farthest next use
                to_evict = max(next_use.items(), key=lambda x: x[1])[0]
                evicted = to_evict
                frames[frames.index(to_evict)] = ref
        timeline.append({'ref': ref, 'frames': frames.copy(), 'hit': hit, 'evicted': evicted})
    hits = len(refs) - faults
    return timeline, {'faults': faults, 'hits': hits, 'hit_ratio': hits/len(refs) if refs else 0}
