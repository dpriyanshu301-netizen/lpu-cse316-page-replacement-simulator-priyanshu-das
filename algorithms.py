# algorithms.py
# Efficient Page Replacement Algorithms
# Author: Priyanshu Das — LPU CSE316

 def simulate_fifo(ref_string, frames):
    timeline = []
    frame_list = [-1] * frames
    pointer = 0
    faults = hits = 0

    for ref in ref_string:
        if ref in frame_list:
            hits += 1
            hit = True
            evicted = None
        else:
            evicted = frame_list[pointer] if frame_list[pointer] != -1 else None
            frame_list[pointer] = ref
            pointer = (pointer + 1) % frames
            faults += 1
            hit = False

        timeline.append({
            "ref": ref,
            "frames": frame_list.copy(),
            "hit": hit,
            "evicted": evicted
        })

    return timeline, {"faults": faults, "hits": hits, "hit_ratio": (hits / len(ref_string)) if len(ref_string) else 0.0}


def simulate_lru(ref_string, frames):
    timeline = []
    frame_list = []
    faults = hits = 0
    recent = {}

    for i, ref in enumerate(ref_string):
        if ref in frame_list:
            hits += 1
            hit = True
            evicted = None
        else:
            hit = False
            faults += 1
            if len(frame_list) < frames:
                frame_list.append(ref)
                evicted = None
            else:
                # find least recently used
                lru_page = min(frame_list, key=lambda p: recent.get(p, -1))
                idx = frame_list.index(lru_page)
                evicted = frame_list[idx]
                frame_list[idx] = ref

        recent[ref] = i
        # normalize frames for display
        frames_snapshot = frame_list.copy() + [-1] * (frames - len(frame_list))
        timeline.append({
            "ref": ref,
            "frames": frames_snapshot,
            "hit": hit,
            "evicted": evicted
        })

    return timeline, {"faults": faults, "hits": hits, "hit_ratio": (hits / len(ref_string)) if len(ref_string) else 0.0}


def simulate_optimal(ref_string, frames):
    timeline = []
    frame_list = []
    faults = hits = 0

    for i, ref in enumerate(ref_string):
        if ref in frame_list:
            hits += 1
            hit = True
            evicted = None
        else:
            hit = False
            faults += 1
            if len(frame_list) < frames:
                frame_list.append(ref)
                evicted = None
            else:
                future = ref_string[i+1:]
                index_map = {}
                for f in frame_list:
                    if f in future:
                        index_map[f] = future.index(f)
                    else:
                        index_map[f] = float('inf')

                to_replace = max(index_map, key=index_map.get)
                idx = frame_list.index(to_replace)
                evicted = frame_list[idx]
                frame_list[idx] = ref

        frames_snapshot = frame_list.copy() + [-1] * (frames - len(frame_list))
        timeline.append({
            "ref": ref,
            "frames": frames_snapshot,
            "hit": hit,
            "evicted": evicted
        })

    return timeline, {"faults": faults, "hits": hits, "hit_ratio": (hits / len(ref_string)) if len(ref_string) else 0.0}

